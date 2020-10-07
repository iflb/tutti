def db_name_for_nanotasks():
    return "Nanotask"

def db_name_for_answers():
    return "Answer"

def collection_name_for_nanotasks(pn, tn):
    return f"{pn}/{tn}"

def collection_name_for_answers(nsid):
    return nsid

def parsed_collection_name_for_answers(name):
    return name.split("/")

def parsed_collection_name_for_nanotasks(name):
    return name
