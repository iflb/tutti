import boto3
import json

from ducts.event import EventHandler
from ifconf import configure_module, config_callback

from pymongo import MongoClient

import logging
logger = logging.getLogger(__name__)

logging.getLogger('boto3').setLevel(logging.CRITICAL)
logging.getLogger('botocore').setLevel(logging.CRITICAL)
logging.getLogger('nose').setLevel(logging.CRITICAL)

from handler import paths, common
from handler.handler_output import handler_output

class Handler(EventHandler):
    def __init__(self):
        super().__init__()
        self.db = MongoClient()
        self.hits = []

    def setup(self, handler_spec, manager):
        self.mturk = manager.load_helper_module('helper_mturk')
        handler_spec.set_description('テンプレート一覧を取得します。')
        handler_spec.set_as_responsive()
        return handler_spec

    @handler_output
    async def handle(self, event, output):
        async with self.mturk.get_client_async() as client:
            command = event.data[0]
            project_name = event.data[1]
            #options = event.data[2:]

            output.set("Command", command)

            if command=="boto3_raw":
                operation = event.data[1]
                params = json.loads("".join(event.data[2:]))
                output.set("Operation", operation)
                output.set("Params", params)

                try:
                    eval(f"func = await client.{operation}")
                except:
                    raise Exception(f"boto3 operation '{operation}' not found")
                res = func(**params)

                res = self.mturk.datetime_to_unixtime(res)
                output.set("Results", res)

            elif command=="list_all_hits" or (command=="list_all_hits_cached" and len(self.hits)==0):
                self.hits = []
                next_token = None
                while True:
                    if next_token:  res = await client.list_hits(MaxResults=100,NextToken=next_token)
                    else:           res = await client.list_hits(MaxResults=100)

                    for h in res["HITs"]:
                        h["CreationTime"] = h["CreationTime"].timestamp()
                        h["Expiration"] = h["Expiration"].timestamp()

                    self.hits.extend(res["HITs"])

                    if "NextToken" in res:  next_token = res["NextToken"]
                    else:                   break

                output.set("HITs", self.hits)

            elif command=="list_all_hits_cached":
                output.set("HITs", self.hits)

            elif command=="create_hit":
                #is_prod_mode = (options[1]=="production")
                params = {
                    "MaxAssignments": 1,
                    "LifetimeInSeconds": 360000,
                    "AutoApprovalDelayInSeconds": 259200,
                    "AssignmentDurationInSeconds": 36000,
                    "Reward": "0.01",
                    "Title": "My HIT",
                    "Keywords": "susumu",
                    "Description": "this is my test hit"
                }
                params["Question"] = '<ExternalQuestion xmlns="http://mechanicalturk.amazonaws.com/AWSMechanicalTurkDataSchemas/2006-07-14/ExternalQuestion.xsd">'\
                    + '<ExternalURL>{}</ExternalURL>'.format(f"https://saito2.r9n.net/vue/private-prod/{project_name}/")\
                    + '<FrameHeight>{}</FrameHeight>'.format(800)\
                    + '</ExternalQuestion>'
                await client.create_hit(**params)
            else:
                raise Exception(f"unknown command '{command}'")
