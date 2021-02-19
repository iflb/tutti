import os
import asyncio
from datetime import datetime
import xml.etree.ElementTree as ET

from ducts.event import EventHandler

sem_limit = 10

class Handler(EventHandler):
    def __init__(self):
        super().__init__()

    async def setup(self, handler_spec, manager):
        self.evt_mturk_api_core = manager.get_handler_for(manager.key_ids["MTURK_API_CORE"])[1]

        handler_spec.set_description('Lists HITs.')
        handler_spec.set_as_responsive()
        return handler_spec

    async def handle(self, event):
        pass

    async def list_hits(self, Cached=True):
        if Cached and (hits := await self.evt_mturk_api_core.cache_get_hit_list()):
            return hits

        else:
            next_token = None
            hits = {}
            num_hits_retrieved = 0
            while True:
                if next_token:  res = await self.evt_mturk_api_core.exec_boto3("list_hits", { "MaxResults": 100, "NextToken": next_token })
                else:           res = await self.evt_mturk_api_core.exec_boto3("list_hits", { "MaxResults": 100 })

                num_hits_retrieved += res["NumResults"]

                for h in res["HITs"]:
                    htid = h["HITTypeId"]
                    pn = ET.fromstring(h["Question"])[0].text.split("/")[-1]
                    if htid not in hits:
                        hits[htid] = {
                            "ProjectNames": [pn],
                            "Count": 0,
                            "HITIds": [],
                            "HITGroupId": h["HITGroupId"],
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
                            "CreationTime": h["CreationTime"],
                            "Expiration": h["Expiration"],
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

                    if pn not in hits[htid]["ProjectNames"]:
                        hits[htid]["ProjectNames"].append(pn)
                    hits[htid]["Count"] += 1
                    hits[htid]["HITIds"].append(h["HITId"])
                    hits[htid]["HITStatusCount"][h["HITStatus"]] += 1
                    hits[htid]["HITReviewStatusCount"][h["HITReviewStatus"]] += 1

                if ("NextToken" in res): #and ((limit is None) or (limit > num_hits_retrieved)):
                    next_token = res["NextToken"]
                    continue
                else:
                    break

            ret = { "LastRetrieved": datetime.now().timestamp(), "HITTypes": hits }
            await self.evt_mturk_api_core.cache_set_hit_list(ret)
            return ret

    async def get_hit_types(self, HITTypeIds=None):
        if not isinstance(HITTypeIds, list):  HITTypeIds = await self.evt_mturk_api_core.cache_get_hit_type_ids()
        return { htid: await self.evt_mturk_api_core.cache_get_hit_type(htid) for htid in HITTypeIds }

    async def create_hit_type(self, CreateHITTypeParams):
        ret = await self.evt_mturk_api_core.exec_boto3("create_hit_type", CreateHITTypeParams)
        htid = ret["HITTypeId"]
        await self.evt_mturk_api_core.cache_set_hit_type(htid, CreateHITTypeParams)
        return htid

    async def create_hit_with_hit_type(self, ProjectName, NumHITs, CreateHITsWithHITTypeParams, FrameHeight=800):
        sem = asyncio.Semaphore(sem_limit)
        async def _create_hit():
            async with sem:
                return await self.evt_mturk_api_core.exec_boto3("create_hit_with_hit_type", CreateHITsWithHITTypeParams)

        url = f"https://{os.environ['DOMAIN_NAME']}/vue/private-prod/{ProjectName}"
        CreateHITsWithHITTypeParams["Question"] = f'''
            <ExternalQuestion
                xmlns="http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2006-07-14/ExternalQuestion.xsd">
                <ExternalURL>{url}</ExternalURL>
                <FrameHeight>{FrameHeight}</FrameHeight>
            </ExternalQuestion>'''
        tasks = [asyncio.ensure_future(_create_hit()) for i in range(NumHITs)]
        return await asyncio.gather(*tasks)

    async def expire_hits(self, HITIds):
        sem = asyncio.Semaphore(sem_limit)
        async def _expire_hit(HITId):
            async with sem:
                return await self.evt_mturk_api_core.exec_boto3("update_expiration_for_hit", { "HITId": HITId, "ExpireAt": datetime(1,1,1) })

        tasks = [asyncio.ensure_future(_expire_hit(HITId)) for HITId in HITIds]
        return await asyncio.gather(*tasks)

    async def delete_hits(self, HITIds):
        sem = asyncio.Semaphore(sem_limit)
        async def _delete_hit(HITId):
            async with sem:
                return await self.evt_mturk_api_core.exec_boto3("delete_hit", { "HITId": HITId })
                
        tasks = [asyncio.ensure_future(_delete_hit(HITId)) for HITId in HITIds]
        return await asyncio.gather(*tasks)
