def key_nids_for_pn_tn(pn,tn):
    return f"NanotaskIds/PRJ:{pn}/TMPL:{tn}"

def key_wsids_for_pn_wid_ct(pn,wid,ct):
    return f"WorkSessionIds/PRJ:{pn}/WKR:{wid}/CT:{ct}"

def key_nsids_for_wsid(wsid):
    return f"NodeSessionIds/{wsid}"
#def key_nsid_set_for_wsid(wsid):
#    return f"NodeSessionIdsHistory/{wsid}"

def key_wids_for_pn(pn):
    return f"WorkerIds/PRJ:{pn}"

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
