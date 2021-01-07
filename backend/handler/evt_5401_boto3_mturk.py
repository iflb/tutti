from datetime import datetime

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
        self.mturk = manager.load_helper_module('helper_mturk')
        self.redis = manager.redis
        handler_spec.set_description('テンプレート一覧を取得します。')
        handler_spec.set_as_responsive()
        return handler_spec


    @handler_output
    async def handle(self, event, output):
        method = event.data["Method"]
        params = event.data["Parameters"]
        results = await self.exec_boto3(method, params)
        output.set("Results", results)

    async def exec_boto3(self, method, params):
        async with await self.mturk.get_client_async(self.redis) as client:
            namespace = {"client": client}
            exec("async def _func(**kwargs): return await client.{}(**kwargs)".format(method), namespace)
            results = await namespace["_func"](**params)
            self.map_nested_dicts_modify(results, lambda x: x.timestamp() if isinstance(x, datetime) else x)
            return results

    def map_nested_dicts_modify(self, ob, func):
        for k, v in ob.items():
            if isinstance(v, dict):
                self.map_nested_dicts_modify(v, func)
            elif isinstance(v, list):
                for _v in v: self.map_nested_dicts_modify(_v, func)
            else:
                ob[k] = func(v)
