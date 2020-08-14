import asyncio
from asyncio.subprocess import PIPE

import handler.paths as paths

async def get_projects():
    process = await asyncio.create_subprocess_shell("ls {}".format(paths.projects), stdout=PIPE, shell=True)
    val = await process.communicate()
    
    return val[0].decode().split("\n")[:-1]
