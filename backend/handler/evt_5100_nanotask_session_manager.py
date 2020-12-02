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
        self.schemes = self.load_all_project_schemes()

    async def setup(self, handler_spec, manager):
        self.r_nt = NanotaskResource(manager.redis)
        self.r_ws = WorkSessionResource(manager.redis)
        self.r_ns = NodeSessionResource(manager.redis)
        self.r_ans = AnswerResource(manager.redis)

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

    async def _get_next_template_node(self, next_node, wid, pn, wsid):
        while (next_node := next_node.forward(None, None, None)):
            if next_node.is_template():
                avail_nids = await self.r_nt.get_ids_for_pn_tn(pn, next_node.name)
                if len(avail_nids)>0:
                    nid = await self.r_nt.get_first_id_for_pn_tn_wid(pn, next_node.name, wid)
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
            [target, wsid, nsid] = event.data[1:]
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
                else:
                    try:
                        out_ns, out_nsid = await self._get_next_template_node(scheme.flow.get_begin_node(), wid, pn, wsid)
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
                            out_ns, out_nsid = await self._get_next_template_node(scheme.flow.get_node_by_name(ns["NodeName"]), wid, pn, wsid)
                            out_ans = None
                        except SessionEndException as e:
                            output.set("FlowSessionStatus", "Terminated")
                            output.set("TerminateReason", "SessionEnd")
                            return 
                        except UnskippableNodeException as e:
                            output.set("FlowSessionStatus", "Terminated")
                            output.set("TerminateReason", "UnskippableNode")
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
            output.set("Answers", out_ans["Answers"] if out_ans else None)
            output.set("NanotaskId", out_ns["NanotaskId"])
            print(out_ns)
            if out_ns["NanotaskId"] is not None:
                nt = await self.r_nt.get(out_ns["NanotaskId"])
                output.set("IsStatic", False)
                output.set("Props", nt["Props"])
            else:
                output.set("IsStatic", True)

            # FIXME: currently not working
            output.set("HasPrevTemplate", (await self._get_neighboring_template_node_session(out_ns, "prev") is not None))
            output.set("HasNextTemplate", (await self._get_neighboring_template_node_session(out_ns, "next") is not None))

        else:
            raise Exception("unknown command '{}'".format(command))
