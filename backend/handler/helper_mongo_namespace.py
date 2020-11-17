import os
from pymongo import MongoClient

DEFAULT_DB_NAME = "tutti"
CLCT_NAME_NANOTASK = "nanotask"
CLCT_NAME_ANSWER = "answer"

def get_db(host=None, port=27017):
    if host is None:
        host = os.environ.get("MONGODB_ADDRESS")
    return MongoClient(host, port)[DEFAULT_DB_NAME]






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
