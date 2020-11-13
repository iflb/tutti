import boto3
import datetime
import json

import aiobotocore

import helper_redis_namespace as redis_ns

import logging
logger = logging.getLogger(__name__)

#def get_client(redis, region_name="us-east-1", sandbox=True):
#    try:
#        access_key_id = await redis.execute_str("GET", redis_ns.key_mturk_access_key_id())
#        secret_access_key = await redis.execute_str("GET", redis_ns.key_mturk_secret_access_key()).decode()
#        endpoint_url = "https://mturk-requester-sandbox.us-east-1.amazonaws.com" if sandbox else "https://mturk-requester.us-east-1.amazonaws.com"
#        return boto3.client("mturk",
#                            aws_access_key_id = access_key_id,
#                            aws_secret_access_key = secret_access_key,
#                            region_name = region_name,
#                            endpoint_url = endpoint_url)
#    except Exception as e:
#        raise Exception(e)

def get_client_async(redis, region_name="us-east-1", sandbox=True):
    # FIXME:: better method for synchronous connection?
    import redis as r_sync
    address = redis.conf.redis_uri_main.split("//")[1].split(":")[0]
    r = r_sync.Redis(address)

    try:
        session = aiobotocore.get_session()
        access_key_id = r.get(redis_ns.key_mturk_access_key_id())
        secret_access_key = r.get(redis_ns.key_mturk_secret_access_key())
        endpoint_url = "https://mturk-requester-sandbox.us-east-1.amazonaws.com" if sandbox else "https://mturk-requester.us-east-1.amazonaws.com"
        return session.create_client("mturk",
                       aws_access_key_id = access_key_id.decode(),
                       aws_secret_access_key = secret_access_key.decode(),
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
