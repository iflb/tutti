import boto3
import datetime
import json

import aiobotocore

import redis
r = redis.Redis(host="localhost", port=6379, db=0)

import helper_redis_namespace as redis_ns

import logging
logger = logging.getLogger(__name__)

def get_client(region_name="us-east-1", sandbox=True):
    try:
        access_key_id = r.get(redis_ns.key_mturk_access_key_id()).decode()
        secret_access_key = r.get(redis_ns.key_mturk_secret_access_key()).decode()
        endpoint_url = "https://mturk-requester-sandbox.us-east-1.amazonaws.com" if sandbox else "https://mturk-requester.us-east-1.amazonaws.com"
        return boto3.client("mturk",
                            aws_access_key_id = access_key_id,
                            aws_secret_access_key = secret_access_key,
                            region_name = region_name,
                            endpoint_url = endpoint_url)
    except Exception as e:
        raise Exception(e)

def get_client_async(region_name="us-east-1", sandbox=True):
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
