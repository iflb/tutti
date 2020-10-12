import boto3
from pprint import pprint
from IPython import embed

client = boto3.client('mturk',
                      aws_access_key_id = "AKIAJSZE6X3VGVBJRTHA",
                      aws_secret_access_key = "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",
                      region_name = "us-east-1",
                      endpoint_url = "https://mturk-requester-sandbox.us-east-1.amazonaws.com")

next_token = None
hits_by_date = {}
for i in range(10):
    if next_token:
        res = client.list_hits(MaxResults=100,NextToken=next_token)
    else:
        res = client.list_hits(MaxResults=100)
    for hit in res["HITs"]:
        datestr = hit["CreationTime"].date().strftime("%Y-%m-%d")
        if datestr not in hits_by_date:  hits_by_date[datestr] = []
        hits_by_date[datestr].append(hit)
    if "NextToken" in res:
        next_token = res["NextToken"]
    else:
        break

embed()
