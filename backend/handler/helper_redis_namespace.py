#def key_work_session_ids_by_project_name(pn):
#    return f"Project/{pn}/WorkSessionIds"

#def key_work_session_ids_by_worker_id(wid):
#    return f"Worker/{wid}/WorkSessionIds"

def key_client_tokens(wid):
    return f"Worker/{wid}/ClientTokens"

def key_active_work_session_id(client_token):
    return f"ClientToken/{client_token}/ActiveWorkSessionId"

def key_node_session_ids_by_node_id(ndid):
    return f"Node/{ndid}/NodeSessionIds"



def key_node_session_ids_by_work_session_id(wsid):
    return f"WorkSession/{wsid}/NodeSessionIds"

def key_active_node_session_id(wid, wsid):
    return f"WorkSession/{wsid}/ActiveNodeSessionId"

def key_node_session(nsid):
    return f"NodeSession/{nsid}"

#def key_work_session(wsid):
#    return f"WorkSession/{wsid}"


def key_event_query(eid):
    return f"EventQuery/{eid}"


def key_mturk_access_key_id():
    return f"MTurkAccessKeyId"

def key_mturk_secret_access_key():
    return f"MTurkSecretAccessKey"
