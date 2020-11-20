def key_work_session_ids_by_project_name(pn):
    return f"WorkSessionIds/PRJ:{pn}"
def key_work_session_ids_by_worker_id(wid):
    return f"WorkSessionIds/WKR:{wid}"

def key_node_session_ids_by_project_name_template_name(pn,tn):
    return f"NodeSessionIds/PRJ:{pn}/TMPL:{tn}"
def key_node_session_ids_by_work_session_id(wsid):
    return f"NodeSessionIds/WS:{wsid}"
def key_node_session_ids_by_worker_id(wid):
    return f"NodeSessionIds/WKR:{wid}"

def key_work_session_history_for_worker_id(wid):
    return f"WorkSessionIdHistory/WKR:{wid}"
def key_node_session_history_for_work_session_id(wsid):
    return f"NodeSessionIdHistory/WS:{wsid}"

def key_nanotask_ids_by_project_name_template_name(pn,tn):
    return f"NanotaskIds/PRJ:{pn}/TMPL:{tn}"

def key_answer_ids_by_nanotask_id(nid):
    return f"AnswerIds/NT:{nid}"
def key_answer_ids_by_template_name(pn, tn):
    return f"AnswerIds/PRJ:{pn}/TMPL:{tn}"




async def get_nanotask_ids_for_project_name_template_name(r, pn, tn):
    return await r.execute_str("SMEMBERS", key_nanotask_ids_by_project_name_template_name(pn,tn))

async def get_answer_ids_for_nanotask_id(r, nid):
    return await r.execute_str("SMEMBERS", key_answer_ids_by_nanotask_id(nid))
async def get_answer_ids_for_project_name_template_name(r, pn, tn):
    return await r.execute_str("SMEMBERS", key_answer_ids_by_template_name(pn, tn))

async def register_work_session_id(r, wsid, pn, wid):
    await r.execute("SADD", key_work_session_ids_by_project_name(pn), wsid)
    await r.execute("SADD", key_work_session_ids_by_worker_id(wid), wsid)
    await add_work_session_history_for_worker_id(r, wsid, wid)

async def register_node_session_id(r, nsid, pn, tn, wsid, wid):
    await r.execute("SADD", key_node_session_ids_by_project_name_template_name(pn,tn), nsid)
    await r.execute("SADD", key_node_session_ids_by_work_session_id(wsid), nsid)
    await r.execute("SADD", key_node_session_ids_by_worker_id(wid), nsid)
    await add_node_session_history_for_work_session_id(r, nsid, wsid)

async def register_answer_id(r, aid, pn, tn, nid):
    if nid: await r.execute("SADD", key_answer_ids_by_nanotask_id(nid), aid)
    await r.execute("SADD", key_answer_ids_by_template_name(pn, tn), aid)

async def get_all_node_session_ids(r, pn=None, tn=None, wsid=None, wid=None):
    try:
        if pn and tn:
            assert not (wsid or wid)
            return await r.execute_str("SMEMBERS", key_node_session_ids_by_project_name_template_name(pn,tn))
        elif wsid:
            assert not ((pn and tn) or wid)
            return await r.execute_str("SMEMBERS", key_node_session_ids_by_work_session_id(wsid))
        elif wid:
            assert not ((pn and tn) or wsid)
            return await r.execute_str("SMEMBERS", key_node_session_ids_by_worker_id(wid))
    except:
        raise Exception("confused keys for node session ids")

async def get_all_nanotask_ids(r, pn, tn):
    return await r.execute_str("SMEMBERS", key_nanotask_ids_by_project_name_template_name(pn,tn))
async def add_nanotask_ids(r, pn, tn, nids):
    return await r.execute("SADD", key_nanotask_ids_by_project_name_template_name(pn,tn), *nids)

async def add_work_session_history_for_worker_id(r, wsid, wid):
    await r.execute("XADD", key_work_session_history_for_worker_id(wid), "*", "WorkSessionId", wsid)
async def add_node_session_history_for_work_session_id(r, nsid, wsid):
    await r.execute("XADD", key_node_session_history_for_work_session_id(wsid), "*", "NodeSessionId", nsid)



#async def enqueue_global_assignable_queue(r, score, nid, pn, tn):
#    await r.execute("ZADD", key_global_assignable_nanotask_queue_for_project_name_template_name(pn, tn), score, nid)
#async def dequeue_global_assignable_queue(r, nid, pn, tn):
#    await r.execute("ZREM", key_global_assignable_nanotask_queue_for_project_name_template_name(pn, tn), nid)
#async def copy_global_assignable_queue_to_local(r, pn, tn, wid):
#    await r.execute("EVAL", "for i,v in ipairs(redis.call('zrange', KEYS[1], 0, -1)) do redis.call('zadd', KEYS
#    [2], redis.call('zscore', KEYS[1], v), v) end", 2, key_global_assignable_nanotask_queue_for_project_name_template_name(pn, tn), key_assignable_nanotask_queue_for_project_name_template_name_worker_id(pn, tn, wid))
#async def dequeue_local_assignable_queue(r, nid, pn, tn):
#    await r.execute("ZREM", key_assignable_nanotask_queue_for_project_name_template_name(pn, tn), nid)
#
#def key_global_assignable_nanotask_queue_for_project_name_template_name(pn, tn):
#    return "AssignableNanotaskIdQueue/PRJ:{pn}/TMPL:{tn}"
#
#def key_assignable_nanotask_queue_for_project_name_template_name_worker_id(pn, tn, wid):
#    return "AssignableNanotaskIdQueue/PRJ:{pn}/TMPL:{tn}/WKR:{wid}"


#def key_node_session_ids_by_work_session_id(wsid):
#    return f"WorkSession/{wsid}/NodeSessionIds"




def key_client_tokens(wid):
    return f"Worker/{wid}/ClientTokens"

def key_active_work_session_id(client_token):
    return f"ClientToken/{client_token}/ActiveWorkSessionId"

def key_node_session_ids_by_node_id(ndid):
    return f"Node/{ndid}/NodeSessionIds"


def key_active_node_session_id(wid, wsid):
    return f"WorkSession/{wsid}/ActiveNodeSessionId"

def key_node_session(nsid):
    return f"NodeSession/{nsid}"
def key_node_session_answer_id(nsid):
    return f"NodeSession/{nsid}/AnswerId"



def key_event_query(eid):
    return f"EventQuery/{eid}"


def key_mturk_access_key_id():
    return f"MTurkAccessKeyId"

def key_mturk_secret_access_key():
    return f"MTurkSecretAccessKey"
