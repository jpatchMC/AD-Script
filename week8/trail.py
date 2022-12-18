#!/usr/bin/env python3
from urllib import response
import boto3
import s3enforce
import json

sts_client = boto3.client("sts")
account_id = sts_client.get_caller_identity()["Account"]

def CreateTrail(trail_name,bucket_name):
    trail = boto3.client('cloudtrail')
    try:
        create_response = trail.create_trail(Name=trail_name, S3BucketName=bucket_name)
        log_response = trail.start_logging(Name=trail_name)
        return log_response
    except trail.exceptions.TrailAlreadyExistsException as error:
        return "Trail already exists"
    except:
        return "some other error"

def main():
    bucket_name = "jpatch1-trail-bucket"
    trail_name = "demo-cloud-trail"

    create_response = s3enforce.CreateBucket(bucket_name) # otherscript.functionwithin, pass in the name in ()

    policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "AWSCloudTrailAclCheck20150319",
                "Effect": "Allow",
                "Principal": {"Service": "cloudtrail.amazonaws.com"},
                "Action": "s3:GetBucketAcl",
                "Resource": f"arn:aws:s3:::{bucket_name}"
            },
            {
                "Sid": "AWSCloudTrailWrite20150319",
                "Effect": "Allow",
                "Principal": {"Service": "cloudtrail.amazonaws.com"},
                "Action": "s3:PutObject",
                "Resource": f"arn:aws:s3:::{bucket_name}/AWSLogs/{account_id}/*",
                "Condition": {"StringEquals": {"s3:x-amz-acl": "bucket-owner-full-control"}}
            }
        ]
    }
    bucket_policy_response = s3enforce.SetBucketPolicy(bucket_name,json.dumps(policy)) #otherscript.functionwithin (var with name , change from json(var with policy)) the "Policy" that i'd see on the documentation is already expecting vars with the names i've set
    response = CreateTrail(trail_name,bucket_name)
    print(response)
if __name__ == "__main__":
    main()