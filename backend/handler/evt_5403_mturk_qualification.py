from ducts.event import EventHandler
from ifconf import configure_module, config_callback

import logging
logger = logging.getLogger(__name__)

logging.getLogger('boto3').setLevel(logging.CRITICAL)
logging.getLogger('botocore').setLevel(logging.CRITICAL)
logging.getLogger('nose').setLevel(logging.CRITICAL)

from handler import paths, common
from handler.handler_output import handler_output, CommandError

class Handler(EventHandler):
    def __init__(self):
        super().__init__()

    def setup(self, handler_spec, manager):
        self.namespace_redis = manager.load_helper_module('helper_redis_namespace')
        self.mturk = manager.load_helper_module('helper_mturk')
        handler_spec.set_description('テンプレート一覧を取得します。')
        handler_spec.set_as_responsive()
        return handler_spec

    @handler_output
    async def handle(self, event, output):
        async with await self.mturk.get_client_async(event.session.redis) as client:
            command = event.data["Command"]
            output.set("Command", command)

            if command=="List":
                next_token = None
                quals = []
                while True:
                    kwargs = {
                        "MustBeRequestable": False,
                        "MustBeOwnedByCaller": True
                    }
                    if next_token:  kwargs["NextToken"] = next_token
                    res = await client.list_qualification_types(**kwargs)
                    quals[:0] = [self.mturk.datetime_to_unixtime(q) for q in res["QualificationTypes"]]
                    if "NextToken" in res:
                        next_token = res["NextToken"]
                        continue
                    else:
                        break
                output.set("QualificationTypes", quals)

            elif command=="Create":
                params = event.data["Params"]
                res = await client.create_qualification_type(**params)
                output.set("QualificationType", self.mturk.datetime_to_unixtime(res["QualificationType"]))

            elif command=="Update":
                params = event.data["Params"]
                res = await client.update_qualification_type(**params)
                output.set("QualificationType", self.mturk.datetime_to_unixtime(res["QualificationType"]))

            elif command=="Get":
                qid = event.data["QualificationTypeId"]
                res = await client.get_qualification_type(QualificationTypeId=qid)
                output.set("QualificationType", self.mturk.datetime_to_unixtime(res["QualificationType"]))

            elif command=="GetWorkers":
                qids = event.data["QualificationTypeIds"]
                quals = {}
                for qid in qids:
                    next_token = None
                    quals[qid] = []
                    while True:
                        if next_token:  res = await client.list_workers_with_qualification_type(QualificationTypeId=qid, NextToken=next_token, MaxResults=100)
                        else:           res = await client.list_workers_with_qualification_type(QualificationTypeId=qid, MaxResults=100)
                        quals[qid].extend([self.mturk.datetime_to_unixtime(q) for q in res["Qualifications"]])
                        if "NextToken" in res:
                            logger.debug(res["NextToken"])
                            next_token = res["NextToken"]
                        else:
                            break
                output.set("Qualifications", quals)

            elif command=="delete":
                qid = event.data[1]
                await client.delete_qualification_type(QualificationTypeId=qid)
