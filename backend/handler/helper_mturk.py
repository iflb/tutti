import boto3
import datetime
import json

import aiobotocore

from handler.redis_resource import MTurkResource

import logging
logger = logging.getLogger(__name__)

async def get_client_async(redis, access_key_id=None, secret_access_key=None, region_name="us-east-1", sandbox=None):
    r_mt = MTurkResource(redis)
    try:
        session = aiobotocore.get_session()
        if not access_key_id:
            access_key_id = await r_mt.get_access_key_id()
        if not secret_access_key:
            secret_access_key = await r_mt.get_secret_access_key()
        if not sandbox:
            sandbox = await r_mt.get_is_sandbox()

        if sandbox:  endpoint_url = "https://mturk-requester-sandbox.us-east-1.amazonaws.com"
        else:        endpoint_url = "https://mturk-requester.us-east-1.amazonaws.com"

        return session.create_client("mturk",
                       aws_access_key_id = access_key_id,
                       aws_secret_access_key = secret_access_key,
                       region_name = region_name,
                       endpoint_url = endpoint_url)
    except Exception as e:
        raise Exception(e)


def datetime_to_unixtime(dct):
    for key,val in dct.items():
        if isinstance(val, datetime.date):
            dct[key] = val.timestamp()
        elif isinstance(val, dict):
            dct[key] = datetime_to_unixtime_rec(val)
    return dct


class MTurkSchemaParam:
    def __init__(self, dtype, default=None):
        self.dtype = dtype
        self.default = default

    def json(self, lang):
        ret = { "dtype": self.lang_dtype(lang) }
        if self.default is not None:  ret["default"] = self.default
        return ret  

    def lang_dtype(self, lang):
        if lang=="javascript":
            if self.dtype==int or self.dtype==float:
                return "number"
            elif self.dtype==str:
                return "string"
        else:
            raise Exception(f"unknown language to convert: {lang}")

#class MTurkSchemaParamDataType:
#    def __init__(self, _type):
#        self.type = _type

#class NumberDataType(MTurkSchemaParamDType):
#    pass 

class MTurkSchema:
    def json(self, lang):
        return {k: v.json(lang) for k,v in self.__dict__.items()}

class ListHitsSchema(MTurkSchema):
    def __init__(self):
        self.NextToken = MTurkSchemaParam(str, None)
        self.MaxResults = MTurkSchemaParam(int, None)
