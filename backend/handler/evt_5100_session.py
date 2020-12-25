import importlib.util
from importlib import reload
import inspect

from ducts.event import EventHandler

from handler import common
from handler.handler_output import handler_output

import logging
logger = logging.getLogger(__name__)

from libs.scheme.flow import SessionEndException, UnskippableNodeException
from libs.scheme.client import WorkerClient, WorkSessionClient
from handler.redis_resource import (WorkerResource,
                                    NanotaskResource,
                                    WorkSessionResource,
                                    NodeSessionResource,
                                    AnswerResource)

class Handler(EventHandler):
    def __init__(self):
        super().__init__()
        self.schemes = self.load_all_project_schemes()

    async def setup(self, handler_spec, manager):
        self.r_wkr = WorkerResource(manager.redis)
        self.r_nt = NanotaskResource(manager.redis)
        self.r_ws = WorkSessionResource(manager.redis)
        self.r_ns = NodeSessionResource(manager.redis)
        self.r_ans = AnswerResource(manager.redis)
        self.redis = manager.redis

        handler_spec.set_description('テンプレート一覧を取得します。')
        handler_spec.set_as_responsive()

        return handler_spec

    def load_all_project_schemes(self):
        schemes = {}
        for project_name in common.get_projects():
            try:
                schemes[project_name] = self.load_project_scheme(project_name)
            except Exception as e:
                logger.error(str(e))
        return schemes

    def load_project_scheme(self, project_name):
        try:
            module = "projects.{}.scheme".format(project_name)
            mod_flow = importlib.import_module(module)
            importlib.reload(mod_flow)
            scheme = mod_flow.ProjectScheme()
            return scheme
        except Exception as e:
            raise Exception(f"could not load scheme for {module}: {str(e)}")

    def get_batch_info_dict(self, child):
        if child.is_template():
            return {
                "statement": child.statement.value,
                "condition": inspect.getsource(child.condition) if child.condition else None,
                "is_skippable": child.is_skippable,
                "name": child.name
            }
        else:
            _info = []
            for c in child.children:
                _info.append(self.get_batch_info_dict(c))
            return {
                "name": child.name,
                "statement": child.statement.value,
                "condition": inspect.getsource(child.condition) if child.condition else None,
                "is_skippable": child.is_skippable,
                "children": _info
            }

    async def _get_next_template_node(self, flow, next_node, wid, pn, wsid, nsid):
        prev_nsid = nsid
        wkr_client = await WorkerClient(self.redis, wid, flow.pn)._load_for_read(flow)
        ws_client = await WorkSessionClient(self.redis, wsid, flow.pn)._load_for_read(flow)
        while (next_node := next_node.forward(wkr_client, ws_client)):
            if next_node.is_template():
                has_nanotasks = await self.r_nt.check_id_exists_for_pn_tn(pn, next_node.name)
                if has_nanotasks:
                    asmt_order = self.schemes[pn].assignment_order
                    sort_order = self.schemes[pn].sort_order
                    nid = await self.r_nt.get_first_id_for_pn_tn_wid(pn, next_node.name, wid, assignment_order=asmt_order, sort_order=sort_order)
                    if not nid:  continue
                else:
                    nid = None
            else:
                nid = None
            #else:
            #    continue
            ns = NodeSessionResource.create_instance(pn=pn,
                                                     name=next_node.name,
                                                     wid=wid,
                                                     wsid=wsid,
                                                     nid=nid,
                                                     prev_id=prev_nsid,
                                                     is_template=next_node.is_template())
            nsid = await self.r_ns.add(ns)
            await self.r_ns.add_id_to_history_for_wsid(wsid, nsid)

            if prev_nsid:
                prev_ns = await self.r_ns.get(prev_nsid)
                prev_ns["NextId"] = nsid
                await self.r_ns.update(prev_nsid, prev_ns)

            prev_nsid = nsid
            if next_node.is_template():
                return ns, nsid
        raise SessionEndException()
            


    async def _get_neighboring_template_node_session(self, ns, direction):
        _ns = ns
        if direction=="prev":
            while _ns["PrevId"] is not None and (_ns := await self.r_ns.get(_ns["PrevId"])):
                if _ns["IsTemplateNode"]:  return _ns
        elif direction=="next":
            while _ns["NextId"] is not None and (_ns := await self.r_ns.get(_ns["NextId"])):
                if _ns["IsTemplateNode"]:  return _ns
        return None
                
    @handler_output
    async def handle(self, event, output):
        command = event.data["Command"]
        output.set("Command", command)

        if command=="LoadFlow":
            pn = event.data["ProjectName"]

            scheme = self.load_project_scheme(pn)
            self.schemes[pn] = scheme
            output.set("Flow", self.get_batch_info_dict(scheme.flow.root_node))

        elif command=="Create":
            if not (
                    (pn := event.data["ProjectName"]) and
                    (platform := event.data["Platform"]) and
                    (platform_wid := event.data["PlatformWorkerId"]) and
                    (ct := event.data["ClientToken"])
                ):
                raise Exception("ProjectName, Platform, PlatformWorkerId, and ClientToken are required")

            if not (wid := await self.r_wkr.get_id_for_platform(platform, platform_wid)):
                wid = await self.r_wkr.add(WorkerResource.create_instance(platform_wid, platform))

            if not (wsid := await self.r_ws.get_id_for_pn_wid_ct(pn,wid,ct)):
                wsid = await self.r_ws.add(WorkSessionResource.create_instance(pn,wid,ct,platform))
            await event.session.set_session_attribute("WorkSessionId", wsid)

            output.set("WorkSessionId", wsid)
            output.set("WorkerId", wid)
            output.set("Pagination", self.schemes[pn].pagination)
            output.set("InstructionEnabled", self.schemes[pn].instruction)
            if self.schemes[pn].show_title:  output.set("Title", self.schemes[pn].title)

        elif command=="Get":
            target = event.data["Target"]
            wsid = event.data["WorkSessionId"]
            nsid = event.data["NodeSessionId"]

            ws = await self.r_ws.get(wsid)
            if not ws:  raise Exception("No session found")

            pn = ws["ProjectName"]
            wid = ws["WorkerId"]
            scheme = self.schemes[pn]

            out = {}
            if not nsid:
                if (nsid := await self.r_ns.get_id_for_wsid_by_index(wsid, -1)):
                    out_nsid = nsid
                    out_ns = await self.r_ns.get(nsid)
                    out_ans = await self.r_ans.get(nsid)
                    if (nid := out_ns["NanotaskId"]) and (nid not in await self.r_nt.get_ids_assigned_for_pn_tn_wid(pn,out_ns["NodeName"],wid)):
                        # mark current node session Expired=True
                        await self.r_ns.set_expired(out_nsid)
                        # assign another available nanotask
                        out_ns, out_nsid = await self._get_next_template_node(scheme.flow, scheme.flow.get_node_by_name(out_ns["NodeName"]).prev, wid, pn, wsid, None)
                        out_ans = None

                else:
                    try:
                        out_ns, out_nsid = await self._get_next_template_node(scheme.flow, scheme.flow.get_begin_node(), wid, pn, wsid, None)
                        out_ans = None
                    except SessionEndException as e:
                        output.set("WorkSessionStatus", "Terminated")
                        output.set("TerminateReason", "SessionEnd")
                        return 
                    except UnskippableNodeException as e:
                        output.set("WorkSessionStatus", "Terminated")
                        output.set("TerminateReason", "UnskippableNode")
                        return
                        
            else:
                while (ns := await self.r_ns.get(nsid)):
                    if target=="NEXT":
                        if ns["NextId"]:
                            out_nsid = ns["NextId"]
                            out_ns = await self.r_ns.get(ns["NextId"])
                            await self.r_ns.add_id_to_history_for_wsid(wsid, out_nsid)
                            if out_ns["IsTemplateNode"] and out_ns["Expired"]==0:
                                out_ans = await self.r_ans.get(ns["NextId"])
                                break
                            else:
                                nsid = out_nsid
                                continue
                        else:
                            try:
                                out_ns, out_nsid = await self._get_next_template_node(scheme.flow, scheme.flow.get_node_by_name(ns["NodeName"]), wid, pn, wsid, nsid)
                                out_ans = None
                                break
                            except SessionEndException as e:
                                output.set("WorkSessionStatus", "Terminated")
                                output.set("TerminateReason", "SessionEnd")
                                return 
                            except UnskippableNodeException as e:
                                output.set("WorkSessionStatus", "Terminated")
                                output.set("TerminateReason", "UnskippableNode")
                                return
                    elif target=="PREV":
                        if ns["PrevId"]:
                            out_nsid = ns["PrevId"]
                            out_ns = await self.r_ns.get(ns["PrevId"])
                            await self.r_ns.add_id_to_history_for_wsid(wsid, out_nsid)
                            if out_ns["IsTemplateNode"] and out_ns["Expired"]==0:
                                out_ans = await self.r_ans.get(ns["PrevId"])
                                break
                            else:
                                nsid = out_nsid
                                continue
                        else:
                            raise Exception("Unexpected request for previous node session")
                if out_ns is None:
                    raise Exception("Unexpected error for task retrieval")

            output.set("WorkSessionStatus", "Active")
            output.set("NodeSessionId", out_nsid)
            output.set("Template", out_ns["NodeName"])
            output.set("Answers", out_ans["Answers"] if out_ans else None)
            output.set("NanotaskId", out_ns["NanotaskId"])
            if out_ns["NanotaskId"] is not None:
                nt = await self.r_nt.get(out_ns["NanotaskId"])
                output.set("IsStatic", False)
                output.set("Props", nt["Props"])
            else:
                output.set("IsStatic", True)

            output.set("HasPrevTemplate", (await self._get_neighboring_template_node_session(out_ns, "prev") is not None))
            output.set("HasNextTemplate", (await self._get_neighboring_template_node_session(out_ns, "next") is not None))

        elif command=="SetAnswer":
            if not event.data["NodeSessionId"]:  raise Exception(f"node session ID cannot be null")

            wsid = event.data["WorkSessionId"]
            nsid = event.data["NodeSessionId"]

            ns = await self.r_ns.get(nsid)
            pn = ns["ProjectName"]
            wid = ns["WorkerId"]
            nid = ns["NanotaskId"]

            answer = AnswerResource.create_instance(wsid, wid, nid, event.data["Answer"])
            await self.r_ans.add(nsid, answer)
            output.set("SentAnswer", answer)

            scheme = self.schemes[pn]
            node = scheme.flow.get_node_by_name(ns["NodeName"])
            if nid:
                nt = await self.r_nt.get(nid)
                gt = nt["GroundTruths"]
            else:
                gt = None
            
            wkr_client = WorkerClient(event.session.redis, wid, pn)
            ws_client = WorkSessionClient(event.session.redis, wsid, pn)
            if callable(node.on_submit):
                node.on_submit(wkr_client, ws_client, answer["Answers"], gt)
            await wkr_client._register_new_members_to_redis()
            await ws_client._register_new_members_to_redis()

        else:
            raise Exception("unknown command '{}'".format(command))

    async def handle_closed(self, session):
        return   # TODO

        try:
            wsid = await session.get_session_attribute('WorkSessionId')
        except KeyError:
            wsid = None

        if wsid:
            nsid = await self.r_ns.get_id_for_wsid_by_index(wsid, -1)
            ns = await self.r_ns.get(nsid)
            pn = ns["ProjectName"]
            wid = ns["WorkerId"]
            if (nid := ns["NanotaskId"]):
                await self.r_nt.unassign(pn,ns["NodeName"],wid,nid)
