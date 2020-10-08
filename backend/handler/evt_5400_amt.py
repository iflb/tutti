import boto3

from ducts.event import EventHandler
from ifconf import configure_module, config_callback

from pymongo import MongoClient

import logging
logger = logging.getLogger(__name__)

from handler import paths, common
from handler.handler_output import handler_output

class Handler(EventHandler):
    def __init__(self):
        super().__init__()
        self.db = MongoClient()
        self.boto_client = boto3.client('mturk',
                                        aws_access_key_id = "AKIAJSZE6X3VGVBJRTHA",
                                        aws_secret_access_key = "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",
                                        region_name = "us-east-1",
                                        endpoint_url = "https://mturk-requester-sandbox.us-east-1.amazonaws.com")

    def setup(self, handler_spec, manager):
        handler_spec.set_description('テンプレート一覧を取得します。')
        handler_spec.set_as_responsive()
        return handler_spec

    @handler_output
    async def handle(self, event, output):
        command = event.data[0]
        project_name = event.data[1]
        #options = event.data[2:]

        output.set("Command", command)

        if command=="create_hit":
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
            self.boto_client.create_hit(**params)
        else:
            raise Exception(f"unknown command '{command}'")