import random, string
import json
import copy
import importlib.util
from importlib import reload
import inspect
import pickle
import sys
import os
from datetime import datetime

from ducts.event import EventHandler
from ducts.redis import ChannelForMultiConsumer
from ifconf import configure_module, config_callback

from handler import common
from handler.handler_output import handler_output

#from libs.session import WorkSession
from libs.task_resource import DCModel, Project, Template, TaskQueue, Nanotask

import logging
logger = logging.getLogger(__name__)

from libs.scheme.flow import SessionEndException, UnskippableNodeException
from handler.redis_resource import (NanotaskResource,
                                   WorkSessionResource,
                                   NodeSessionResource,
                                   AnswerResource)
import handler.redis_index as ri

class Handler(EventHandler):
    def __init__(self):
        super().__init__()
        #self.flows = self.load_flows()   # {project_name: TaskFlow}
        self.schemes = self.load_all_project_schemes()
        self.wsessions = {}               # {session_id: iterator}

        #self.dcmodel = DCModel()
        #self.nanotasks = {}                     # { nid: Nanotask }
        #self.assignable_nids = set()               # set(nid)
        #self.tqueue = TaskQueue()
        self.wkr_submitted_nids = {}                   # worker_id -> set(nanotask_id)

    async def setup(self, handler_spec, manager):
        self.namespace_redis = manager.load_helper_module('helper_redis_namespace')
        self.r_nt = NanotaskResource(manager.redis)
        self.r_ws = WorkSessionResource(manager.redis)
        self.r_ns = NodeSessionResource(manager.redis)
        self.r_ans = AnswerResource(manager.redis)
        #await self.cache_nanotasks(manager.redis)

        handler_spec.set_description('テンプレート一覧を取得します。')
        handler_spec.set_as_responsive()

        return handler_spec

    #async def nanotask_upload_watcher(self, r):
    #    ch = await r.conn_for_subscription.subscribe(self.namespace_redis.pubsub_key_nanotask_upload_template())
    #    ch = ChannelForMultiConsumer(ch[0], r.loop)
    #    async for message in ch.iter():
    #        message = message.decode()
    #        [pn, tn] = message.split("/")
    #        await self.cache_nanotasks_each(r, pn, tn)

    #async def run(self, manager):
    #    return await self.nanotask_upload_watcher(manager.redis)

    #async def cache_nanotasks_each(self, redis, pn, tn):
    #    nids = await self.r_nt.get_ids_for_pn_tn(pn, tn)
    #    for nid in nids:
    #        nt = await self.r_nt.get(nid)
    #        aids = await self.r_ans.get_ids_for_nid(nid)
    #        if nt["num_assignable"] < len(aids):
    #            await ri.add_completed_nid_for_pn_tn(redis, pn, tn, nid)
    #        for aid in aids:
    #            a = await self.r_ans.get(aid)
    #            wid = a["WorkerId"]
    #            await ri.add_completed_nid_for_pn_tn_wid(redis, pn, tn, wid, nid)

    #async def cache_nanotasks(self, redis):
    #    for pn in common.get_projects():
    #        for tn in common.get_templates(pn):
    #            await self.cache_nanotasks_each(redis, pn, tn)

    #def create_task_queue_for_worker(self, wid):
    #    wkr_assignable_nids = self.assignable_nids - self.wkr_submitted_nids[wid]
    #    for nid in wkr_assignable_nids:
    #        nt = self.nanotasks[nid]
    #        [pn,tn] = [nt.project_name, nt.template_name]
    #        q = self.tqueue.get_queue(wid, pn, tn)
    #        self.tqueue.push(q, nid, nt.priority)

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

    #def load_flow_config(self, project_name):
    #    mod_flow = importlib.import_module("projects.{}.flow".format(project_name))
    #    importlib.reload(mod_flow)
    #    flow = mod_flow.TaskFlow()
    #    flow.root.scan()
    #    return flow

    #def load_flows(self):
    #    flows = {}
    #    for project_name in common.get_projects():
    #        try:
    #            flows[project_name] = self.load_flow_config(project_name)
    #        except Exception as e:
    #            logger.error("could not load flow for {}, {}".format("projects.{}.flow".format(project_name), str(e)))
    #            continue   
    #    return flows

    def get_batch_info_dict(self, child):
        if child.is_template():
            return {
                "statement": child.statement.value,
                "condition": child.condition,
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
                "condition": child.condition,
                "is_skippable": child.is_skippable,
                "children": _info
            }

    @handler_output
    async def handle(self, event, output):
        command = event.data[0]
        output.set("Command", command)

        if command=="LOAD_FLOW":
            pn = event.data[1]

            scheme = self.load_project_scheme(pn)
            self.schemes[pn] = scheme
            output.set("Flow", self.get_batch_info_dict(scheme.flow.root_node))

        elif command=="CREATE_SESSION":
            [pn, wid, ct] = event.data[1:]

            if not (pn and wid and ct):
                raise Exception("ProjectName, WorkerId, and ClientToken are required")

            wsid = await self.r_ws.get_id_for_pn_wid_ct(pn,wid,ct)
            if not wsid:
                wsid = await self.r_ws.add(WorkSessionResource.create_instance(pn,wid,ct))

            output.set("WorkSessionId", wsid)

        elif command=="GET":
            async def _get_next_template_node(next_node, wid, pn):
                while (next_node := next_node.forward(None, None, None)):
                    if next_node.is_template():
                        avail_nids = await self.r_nt.get_ids_for_pn_tn(pn, next_node.name)
                        if len(avail_nids)>0:
                            next_nid = await self.r_nt.get_first_id_for_pn_tn_wid(pn, next_node.name, wid)
                            if not nid:  continue
                        else:
                            nid = None
                    else:
                        continue
                    ns = NodeSessionResource.create_instance(pn=pn,
                                                             name=next_node.name,
                                                             wid=wid,
                                                             wsid=wsid,
                                                             nid=nid,
                                                             prev_id=None,
                                                             is_template=next_node.is_template())
                    nsid = await self.r_ns.add(ns)
                    if next_node.is_template():
                        return ns, nsid
                raise SessionEndException()
                    


            async def _get_neighboring_template_node_session(ns, direction):
                _ns = ns
                if direction=="prev":
                    while _ns["PrevId"] is not None and (_ns := await self.r_ns.get(_ns["PrevId"])):
                        if _ns["IsTemplateNode"]:  return _ns
                elif direction=="next":
                    while _ns["NextId"] is not None and (_ns := await self.r_ns.get(_ns["NextId"])):
                        if _ns["IsTemplateNode"]:  return _ns
                return None
                
            [target, wsid, nsid] = event.data[1:]
            ws = await self.r_ws.get(wsid)
            if not ws:  raise Exception("No session found")

            pn = ws["ProjectName"]
            wid = ws["WorkerId"]

            scheme = self.schemes[pn]

            print(event.data)
            out = {}
            if not nsid:
                if (nsid := await self.r_ns.get_id_for_wsid_by_index(wsid, -1)):
                    out_nsid = nsid
                    out_ns = await self.r_ns.get(nsid)
                    out_ans = await self.r_ans.get(nsid)
                else:
                    try:
                        out_ns, out_nsid = await _get_next_template_node(scheme.flow.get_begin_node(), wid, pn)
                        out_ans = None
                    except SessionEndException as e:
                        output.set("FlowSessionStatus", "Terminated")
                        output.set("TerminateReason", "SessionEnd")
                        return 
                    except UnskippableNodeException as e:
                        output.set("FlowSessionStatus", "Terminated")
                        output.set("TerminateReason", "UnskippableNode")
                        return
                        
            else:
                ns = await self.r_ns.get(nsid)
                if target=="NEXT":
                    if ns["NextId"]:
                        out_nsid = ns["NextId"]
                        out_ns = await self.r_ns.get(ns["NextId"])
                        out_ans = await self.r_ans.get(ns["NextId"])
                        # also record this behavior to history?
                    else:
                        try:
                            out_ns, out_nsid = await _get_next_template_node(scheme.flow.get_node_by_name(ns["NodeName"]), wid, pn)
                            out_ans = None
                        except SessionEndException as e:
                            output.set("FlowSessionStatus", "Terminated")
                            output.set("TerminateReason", "SessionEnd")
                            return 
                        except UnskippableNodeException as e:
                            output.set("FlowSessionStatus", "Terminated")
                            output.set("TerminatedReason", "UnskippableNode")
                            return
                elif target=="PREV":
                    if ns["PrevId"]:
                        out_nsid = ns["PrevId"]
                        out_ns = await self.r_ns.get(ns["PrevId"])
                        out_ans = await self.r_ans.get(ns["PrevId"])
                        # also record this behavior to history?
                    else:
                        raise Exception("Unexpected request for previous node session")

            output.set("FlowSessionStatus", "Active")
            output.set("NodeSessionId", out_nsid)
            output.set("Template", out_ns["NodeName"])
            output.set("Answers", out_ans)
            output.set("NanotaskId", out_ns["NanotaskId"])
            if out_ns["NanotaskId"] is not None:
                nt = await self.r_nt.get(out_ns["NanotaskId"])
                output.set("IsStatic", False)
                output.set("Props", nt["Props"])
            else:
                output.set("IsStatic", True)

            output.set("HasPrevTemplate", (await _get_neighboring_template_node_session(out_ns, "prev") is not None))
            output.set("HasNextTemplate", (await _get_neighboring_template_node_session(out_ns, "next") is not None))


            #ns = None
            #if nsid:
            #    if (ns := ws.get_existing_node_session(nsid)):
            #        [name, id] = [ns.node.name, ns.id]
            #        [p_name, p_id] = [ns.prev.node.name, ns.prev.id]
            #        [n_name, n_id] = [ns.next.node.name, ns.next.id] if ns.next else [None, None]
            #        logger.info(f"IN:: {name}({id}), prev={p_name}({p_id}), next={n_name}({n_id})")
            #    else:
            #        raise Exception(f"Invalid node session ID: {nsid}")

            #if target=="NEXT":
            #    if (not ns) and (ws.current_ns):
            #        out_ns = ws.current_ns
            #        output.set("NodeSessionId", out_ns.id)
            #        output.set("Template", out_ns.node.name)
            #        output.set("Answers", out_ns.answers)
            #        output.set("NanotaskId", out_ns.nid)
            #        if out_ns.nid is not None:
            #            output.set("IsStatic", False)
            #            output.set("Props", self.nanotasks[out_ns.nid].props)
            #        await self.namespace_redis.add_node_session_history_for_work_session_id(event.session.redis, out_ns.id, ws.id)

            #    # get existing node session, when node session is not latest
            #    elif ns and (out_ns := ws.get_neighboring_template_node_session(ns, "next")):
            #        if out_ns != ws.get_existing_node_session(out_ns.id):
            #            raise Exception("Broken consistency of node sessions in work session")
            #        output.set("NodeSessionId", out_ns.id)
            #        output.set("Template", out_ns.node.name)
            #        output.set("Answers", out_ns.answers)
            #        output.set("NanotaskId", out_ns.nid)
            #        if out_ns.nid is not None:
            #            output.set("IsStatic", False)
            #            output.set("Props", self.nanotasks[out_ns.nid].props)
            #        await self.namespace_redis.add_node_session_history_for_work_session_id(event.session.redis, out_ns.id, ws.id)

            #    else:   # create new node session, when work session is initialized OR node session is latest
            #        try:
            #            # if there is no more available template
            #            if not (out_ns := ws.create_next_template_node_session(ns)):
            #                raise StopIteration()

            #            tn = out_ns.node.name
            #            output.set("NodeSessionId", out_ns.id)
            #            output.set("Template", tn)
            #            tmpl = self.dcmodel.get_project(pn).get_template(tn)
            #            if tmpl.has_nanotasks():
            #                q = self.tqueue.get_queue(wid, pn, tn)
            #                if len(q)>0:
            #                    nid = self.tqueue.pop(q)
            #                    out_ns.update_attr("nid", nid)

            #                    nt = self.nanotasks[nid]
            #                    output.set("IsStatic", False)
            #                    output.set("NanotaskId", nid)
            #                    output.set("Props", nt.props)
            #                else:
            #                    output.set("NanotaskId", None)
            #            else:
            #                output.set("IsStatic", True)
            #            await self.namespace_redis.register_node_session_id(event.session.redis, out_ns.id, pn, tn, ws.id, wid)

            #        except StopIteration as e:
            #            output.set("Template", None)

            #elif target=="PREV":
            #    out_ns = ws.get_neighboring_template_node_session(ns, "prev")
            #    if out_ns != ws.get_existing_node_session(out_ns.id):
            #        raise Exception("Broken consistency of node sessions in work session")
            #    
            #    output.set("NodeSessionId", out_ns.id)
            #    output.set("Template", out_ns.node.name)
            #    output.set("Answers", out_ns.answers)
            #    if (nid := out_ns.nid):
            #        output.set("IsStatic", False)
            #        output.set("Props", self.nanotasks[nid].props)
            #    else:
            #        output.set("IsStatic", True)
            #    output.set("NanotaskId", nid)
            #    await self.namespace_redis.add_node_session_history_for_work_session_id(event.session.redis, out_ns.id, ws.id)


            #if out_ns:
            #    ws.current_ns = out_ns
            #    [name, id] = [out_ns.node.name, out_ns.id]
            #    [p_name, p_id] = [out_ns.prev.node.name, out_ns.prev.id]
            #    [n_name, n_id] = [out_ns.next.node.name, out_ns.next.id] if out_ns.next else [None, None]
            #    logger.info(f"OUT:: {name}({id}), prev={p_name}({p_id}), next={n_name}({n_id})")

            #    output.set("HasPrevTemplate", (ws.get_neighboring_template_node_session(out_ns, "prev") is not None))
            #    output.set("HasNextTemplate", (ws.get_neighboring_template_node_session(out_ns, "next") is not None))

                    
        elif command=="ANSWER":
            [wsid, nsid] = event.data[1:3]
            print(event.data)

            ### FIXME
            answers = json.loads(" ".join(event.data[3:]))

            ws = await self.r_ws.get(wsid)
            wid = ws["WorkerId"]
            pn = ws["ProjectName"]

            #ws = self.wsessions[wsid]
            #wid = ws.wid
            #pn = ws.pid

            if nsid=="":
                raise Exception(f"node session ID cannot be null")

            ns = await self.r_ns.get(nsid)
            tn = ns["NodeName"]
            nid = ns["NanotaskId"]

            #ns = ws.get_existing_node_session(nsid)
            #tn = ns.node.name
            #nid = ns.nid
            #ns.answers = answers

            #self.wkr_submitted_nids[wid].add(nid)
            #ans_json = {
            #    "WorkSessionId": wsid,
            #    "NodeSessionId": nsid,
            #    "WorkerId": wid,
            #    "Answers": answers,
            #    "Timestamp": datetime.now().timestamp()
            #}
            #if nid!="null":  ans_json["NanotaskId"] = nid
            #await add_answer_for_nsid(event.session.redis, nsid, ans_json)
            answer = AnswerResource.create_instance(answers)
            print(answer)
            await self.r_ans.add(nsid, answer)
            output.set("SentAnswer", answer)

        else:
            raise Exception("unknown command '{}'".format(command))
