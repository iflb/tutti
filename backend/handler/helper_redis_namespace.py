def key_for_work_session_ids_by_project_name(pn):
    return f"Project/{pn}/WorkSessionId"

def key_for_work_session_ids_by_worker_id(wid):
    return f"Worker/{wid}/WorkSessionId"

def key_for_node_session_ids_by_node_id(ndid):
    return f"Node/{ndid}/NodeSessionId"

def key_for_node_session_ids_by_work_session_id(wsid):
    return f"WorkSession/{wsid}/NodeSessionId"

def key_for_node_session_by_id(nsid):
    return f"NodeSession/{nsid}"
