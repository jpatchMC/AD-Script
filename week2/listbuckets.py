#!/usr/bin/env python3
import boto3
import json
#organize things
import datetime
#date time is strange for json i guess
def defaultconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()
        #convert datetime to readable

client = boto3.client('s3')

response = client.list_buckets()
#print(json.dumps(response,default=defaultconverter,indent=4))

for bucket in response['Buckets']:
    Bname = bucket['Name']
    print(bucket['Name'])
    #with open('mybuckets.txt ','w')as B:
        #B.writelines(bucket['Name'])
    response2 = client.list_objects_v2(
        Bucket=Bname,
    )
    for objects in response2['Contents']:
        print(objects['Key'])
    #with open('mybuckets.txt ','a')as O:
        #O.write(objects['Key'])
#print(json.dumps(response2,default=defaultconverter,indent=4))



