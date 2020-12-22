import os
import json
from pprint import pprint
from datetime import datetime

from ducts.event import EventHandler
from ifconf import configure_module, config_callback

import logging
logger = logging.getLogger(__name__)

logging.getLogger('boto3').setLevel(logging.CRITICAL)
logging.getLogger('botocore').setLevel(logging.CRITICAL)
logging.getLogger('nose').setLevel(logging.CRITICAL)

from handler import paths, common
from handler.handler_output import handler_output, CommandError

from handler.redis_resource import MTurkResource

class Handler(EventHandler):
    def __init__(self):
        super().__init__()

    async def setup(self, handler_spec, manager):
        self.namespace_redis = manager.load_helper_module('helper_redis_namespace')
        self.mturk = manager.load_helper_module('helper_mturk')
        self.r_mt = MTurkResource(manager.redis)
        handler_spec.set_description('テンプレート一覧を取得します。')
        handler_spec.set_as_responsive()
        return handler_spec

    @handler_output
    async def handle(self, event, output):
        command = event.data["Command"]
        output.set("Command", command)
        async with await self.mturk.get_client_async(event.session.redis) as client:
            if command=="List":
                limit = event.data["Limit"] if "Limit" in event.data else None
                cached = event.data["Cached"] if "Cached" in event.data else True

                if cached:
                    hits = await self.r_mt.get_hits()
                    if hits:  output.set("Result", hits)
                    else:     cached = False

                if cached==False:
                    next_token = None
                    hits = {}
                    num_hits_retrieved = 0
                    while True:
                        if next_token:  res = await client.list_hits(NextToken=next_token,MaxResults=100)
                        else:           res = await client.list_hits(MaxResults=100)

                        num_hits_retrieved += res["NumResults"]

                        for h in res["HITs"]:
                            htid = h["HITTypeId"]
                            if htid not in hits:
                                hits[htid] = {
                                    "Count": 0,
                                    "HITIds": [h["HITId"]],
                                    "Props": {
                                        k: h[k] for k in (
                                            "AutoApprovalDelayInSeconds",
                                            "AssignmentDurationInSeconds",
                                            "Reward",
                                            "Title",
                                            "Keywords",
                                            "Description",
                                            "QualificationRequirements"
                                        ) if k in h
                                    },
                                    "CreationTime": h["CreationTime"].timestamp(),
                                    "Expiration": h["Expiration"].timestamp(),
                                    "HITStatusCount": {
                                        "Assignable": 0,
                                        "Unassignable": 0,
                                        "Reviewable": 0,
                                        "Reviewing": 0,
                                        "Disposed": 0
                                    },
                                    "HITReviewStatusCount": {
                                        "NotReviewed": 0,
                                        "MarkedForReview": 0,
                                        "ReviewedAppropriate": 0,
                                        "ReviewedInappropriate": 0
                                    }
                                }

                            hits[htid]["Count"] += 1
                            hits[htid]["HITIds"].append(h["HITId"])
                            hits[htid]["HITStatusCount"][h["HITStatus"]] += 1
                            hits[htid]["HITReviewStatusCount"][h["HITReviewStatus"]] += 1

                        if ("NextToken" in res) and ((limit is None) or (limit > num_hits_retrieved)):
                            next_token = res["NextToken"]
                            continue
                        else:
                            break

                    ret = { "LastRetrieved": datetime.now().timestamp(), "HITTypes": hits }
                    await self.r_mt.set_hits(ret)
                    output.set("Result", ret)

            elif command=="ListHITTypes":
                htids = await self.r_mt.get_hit_type_ids()
                hts = {htid:await self.r_mt.get_hit_type_params_for_htid(htid) for htid in htids}
                output.set("HITTypes", hts)

            elif command=="LoadHITType":
                htid = event.data["HITTypeId"]
                params = await self.r_mt.get_hit_type_params_for_htid(htid)
                output.set("HITTypeParams", params)

            elif command=="CreateHITType":
                params = event.data["Params"]
                ret = await client.create_hit_type(**params)
                htid = ret["HITTypeId"]
                await self.r_mt.set_hit_type_params_for_htid(htid, params)
                output.set("HITTypeId", htid)

            elif command=="CreateHITWithHITType":
                params = event.data["Params"]
                pn = event.data["ProjectName"]
                url = f"https://{os.environ['DOMAIN_NAME']}/vue/private-prod/{pn}"
                frame_height = 800
                params["Question"] = f'''
                    <ExternalQuestion
                        xmlns="http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2006-07-14/ExternalQuestion.xsd">
                        <ExternalURL>{url}</ExternalURL>
                        <FrameHeight>{frame_height}</FrameHeight>
                    </ExternalQuestion>'''
                num = event.data["NumHITs"]
                print(params)
                for i in range(num):
                    res = await client.create_hit_with_hit_type(**params)

            elif command=="update":
                params = json.loads(event.data[1])
                res = await self.client.update_qualification_type(**params)
                output.set("QualificationType", self.mturk.datetime_to_unixtime(res["QualificationType"]))

            elif command=="get":
                qid = event.data[1]
                res = await self.client.get_qualification_type(QualificationTypeId=qid)
                output.set("QualificationType", self.mturk.datetime_to_unixtime(res["QualificationType"]))

            elif command=="get_workers":
                qids = event.data[1:]
                quals = {}
                for qid in qids:
                    next_token = None
                    quals[qid] = []
                    while True:
                        if next_token:  res = await self.client.list_workers_with_qualification_type(QualificationTypeId=qid, NextToken=next_token, MaxResults=100)
                        else:           res = await self.client.list_workers_with_qualification_type(QualificationTypeId=qid, MaxResults=100)
                        quals[qid].extend([self.mturk.datetime_to_unixtime(q) for q in res["Qualifications"]])
                        if "NextToken" in res:
                            logger.debug(res["NextToken"])
                            next_token = res["NextToken"]
                        else:
                            break
                output.set("Qualifications", quals)

            elif command=="delete":
                qid = event.data[1]
                await self.client.delete_qualification_type(QualificationTypeId=qid)

            else:
                raise Exception(f"unknown command '{command}'")
