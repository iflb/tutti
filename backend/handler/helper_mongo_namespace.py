import os
from pymongo import MongoClient
from bson.objectid import ObjectId

DEFAULT_DB_NAME = "tutti"
CLCT_NAME_NANOTASK = "nanotask"
CLCT_NAME_ANSWER = "answer"

def get_db(host=None, port=27017):
    if host is None:
        host = os.environ.get("MONGODB_ADDRESS")
    return MongoClient(host, port)[DEFAULT_DB_NAME]

def wrap_obj_id(data):
    try:
        if data:
            if isinstance(data, list):
                if isinstance(data[0], dict):
                    [d.update({"_id": ObjectId(d["_id"])}) for d in data]
                else:
                    data = [ObjectId(d) for d in data]
            elif isinstance(data, dict):
                data.update({"_id": ObjectId(data["_id"])})
            else:
                data = ObjectId(data)
        return data

    except:
        raise Exception("unsupported data type for wrap_obj_id()")

def unwrap_obj_id(data):
    try:
        if data:
            if isinstance(data, list):
                if isinstance(data[0], dict):
                    [d.update({"_id": str(d["_id"])}) for d in data]
                else:
                    data = [str(d) for d in data]
            elif isinstance(data, dict):
                data.update({"_id": str(data["_id"])})
            else:
                data = str(data)
        return data

    except:
        raise Exception("unsupported data type for unwrap_obj_id()")



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
