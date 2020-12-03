def key_nids_for_pn_tn(pn,tn):
    return f"NanotaskIds/PRJ:{pn}/TMPL:{tn}"

def key_wsid_for_pn_wid_ct(pn,wid,ct):
    return f"WorkSessionIds/PRJ:{pn}/WKR:{wid}/CT:{ct}"

def key_nsid_list_for_wsid(wsid):
    return f"NodeSessionIds/{wsid}"
#def key_nsid_set_for_wsid(wsid):
#    return f"NodeSessionIdsHistory/{wsid}"

def key_aids_for_nid(nid):
    return f"AnswerIds/{nid}"
def key_aids_for_pn_tn(pn,tn):
    return f"AnswerIds/PRJ:{pn}/TMPL:{tn}"

def key_completed_nids_for_pn_tn_wid(pn,tn,wid):
    return f"CompletedNanotaskIds/PRJ:{pn}/TMPL:{tn}/WKR:{wid}"
def key_completed_nids_for_pn_tn(pn,tn):
    return f"CompletedNanotaskIds/PRJ:{pn}/TMPL:{tn}"

def key_assignable_nids_for_pn_tn_wid(pn,tn,wid):
    return f"AssignableNanotaskIds/PRJ:{pn}/TMPL:{tn}/WKR:{wid}"


def key_mturk_access_key_id():
    return f"Platform/AMT/AccessKeyId"
def key_mturk_secret_access_key():
    return f"Platform/AMT/SecretAccessKey"
def key_mturk_is_sandbox():
    return f"Platform/AMT/IsSandbox"

def key_mturk_hit_types(access_key_id):
    return f"Platform/AMT/HITTypes/{access_key_id}"
