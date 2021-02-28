from datetime import datetime

import aiobotocore
import backoff
from botocore.exceptions import ClientError

from ducts.event import EventHandler
from ifconf import configure_module, config_callback

import logging
logger = logging.getLogger(__name__)

logging.getLogger('boto3').setLevel(logging.CRITICAL)
logging.getLogger('botocore').setLevel(logging.CRITICAL)
logging.getLogger('nose').setLevel(logging.CRITICAL)

from handler.handler_output import handler_output
from handler.redis_resource import MTurkResource

class Handler(EventHandler):
    def __init__(self):
        super().__init__()
        self.hits = []

    def setup(self, handler_spec, manager):
        self.r_mt = MTurkResource(manager.redis)

        handler_spec.set_description('Core event for boto3 execution')
        handler_spec.set_as_responsive()
        return handler_spec

    async def handle(self, event):
        pass

    async def cache_get_access_key_id(self):
        return await self.r_mt.get_access_key_id()
    async def cache_get_secret_access_key(self):
        return await self.r_mt.get_secret_access_key()
    async def cache_get_is_sandbox(self):
        return await self.r_mt.get_is_sandbox()
    async def cache_get_hit_list(self):
        return await self.r_mt.get_hits()
    async def cache_set_hit_list(self, data):
        await self.r_mt.set_hits(data)
    async def cache_get_hit_type_ids(self):
        return await self.r_mt.get_hit_type_ids()
    async def cache_get_hit_type(self, HITTypeId):
        return await self.r_mt.get_hit_type_params_for_htid(HITTypeId)
    async def cache_set_hit_type(self, HITTypeId, Params):
        await self.r_mt.set_hit_type_params_for_htid(HITTypeId, Params)
    async def cache_get_hit_type_qualification_type_id(self, HITTypeId):
        await self.r_mt.get_hit_type_qualification_type_id_for_htid(HITTypeId)
    async def cache_set_hit_type_qualification_type_id(self, HITTypeId, QualificationTypeId):
        await self.r_mt.set_hit_type_qualification_type_id_for_htid(HITTypeId, QualificationTypeId)
    async def cache_get_assignments_list(self):
        return await self.r_mt.get_assignments()
    async def cache_set_assignments_list(self, data):
        await self.r_mt.set_assignments(data)

    @backoff.on_predicate(backoff.expo, lambda x: isinstance(x,ClientError))
    async def exec_boto3(self, Method, Parameters=None):
        if Parameters is None:  Parameters = {}

        async with await self._get_client_async() as client:
            namespace = {"client": client}
            exec("async def _func(**kwargs): return await client.{}(**kwargs)".format(Method), namespace)
            try:
                results = await namespace["_func"](**Parameters)
            except ClientError as e:
                if e.response["Error"]["Code"]=="ThrottlingException" and e.response["Error"]["Message"]=="Rate exceeded":
                    return e
                else:
                    raise e
            self.map_nested_dicts_modify(results, lambda x: x.timestamp() if isinstance(x, datetime) else x)
            return results

    async def _get_client_async(self, access_key_id=None, secret_access_key=None, region_name="us-east-1", sandbox=None):
        try:
            session = aiobotocore.get_session()
            if not access_key_id:
                access_key_id = await self.cache_get_access_key_id()
            if not secret_access_key:
                secret_access_key = await self.cache_get_secret_access_key()
            if not sandbox:
                sandbox = await self.cache_get_is_sandbox()
    
            if sandbox:  endpoint_url = "https://mturk-requester-sandbox.us-east-1.amazonaws.com"
            else:        endpoint_url = "https://mturk-requester.us-east-1.amazonaws.com"

            return session.create_client("mturk",
                           aws_access_key_id = access_key_id,
                           aws_secret_access_key = secret_access_key,
                           region_name = region_name,
                           endpoint_url = endpoint_url)
        except Exception as e:
            raise Exception(e)

    def map_nested_dicts_modify(self, ob, func):
        if isinstance(ob, dict):
            for k, v in ob.items():
                if isinstance(v, dict):
                    self.map_nested_dicts_modify(v, func)
                elif isinstance(v, list):
                    for _v in v: self.map_nested_dicts_modify(_v, func)
                else:
                    ob[k] = func(v)
        elif isinstance(ob, list):
            for i,v in enumerate(ob):
                if isinstance(v, dict):
                    self.map_nested_dicts_modify(v, func)
                elif isinstance(v, list):
                    for _v in v: self.map_nested_dicts_modify(_v, func)
                else:
                    ob[i] = func(v)

