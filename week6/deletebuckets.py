#!/usr/bin/env python3

import boto3
s3 = boto3.client('s3')

response = s3.list_buckets()

for bucket in response['Buckets']:
    print(f"deleting bucket {bucket['Name']}")
    obj_response = s3.list_objects_v2(Bucket=bucket['Name'])
    if obj_response.get('Contents'):
        for object in obj_response['Contents']:
            print(f"...Deleting {object['Key']}")
            del_obj_response = s3.delete_object(Bucket=bucket['Name'],Key=object['Key'])
    del_buck_response = s3.delete_bucket(Bucket=bucket['Name'])