import boto3
from pprint import pprint
from IPython import embed

info = {
    "aws_access_key_id": "",
    "aws_secret_access_key": "",
    "region_name": "us-east-1",
    #"endpoint_url": "https://mturk-requester-sandbox.us-east-1.amazonaws.com"
}

iam = boto3.resource('iam', **info)

print(iam)

##client = boto3.client('iam', **info)
#username = "hoge"
#client.create_user(UserName=username)
#res = client.create_access_key(UserName=username)
#akid = res["AccessKey"]["AccessKeyId"]
#sakey = res["AccessKey"]["SecretAccessKey"]
#print(akid, sakey)
