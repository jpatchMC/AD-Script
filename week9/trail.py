#!/usr/bin/env python3

import boto3
import s3enforce
import json
import time

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

def StartLogging(trail_name):
    trail = boto3.client('cloudtrail')
    response = trail.start_logging(Name=trail_name)
    return response
def StopLogging(trail_name):
    trail = boto3.client('cloudtrail')
    response = trail.stop_logging(Name=trail_name)
    return response

def GetTrailStatus(trail_name):
    trail = boto3.client('cloudtrail')
    try:
        response = trail.get_trail_status(Name=trail_name)
        #print(response)
        return response['IsLogging'] #element that gets returned from that object
    except trail.exceptions.TrailNotFoundException as error:
        print("That trail name does not exist")
        raise NameError("That Cloudtrail Trail was not found") #whats raise and where does NameError come from?
    except:
        print("Some other error occurred")

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
    response = CreateTrail(trail_name,bucket_name) #start created trail
    stop_response = StopLogging(trail_name) #issue a wait
    time.sleep(2)
    #print(GetTrailStatus(trail_name))
    if GetTrailStatus(trail_name): #this is just yes or no
        print("Trail is logging as expected")
    else:
        print("Trail is NOT logging, something is up.")
    print(response)
if __name__ == "__main__":
    main()