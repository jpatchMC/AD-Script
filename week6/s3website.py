#!/usr/bin/env python3
import boto3
import json
#organize things
import datetime
#date time is strange for json i guess
import random, argparse, string,botocore

from yaml import parse
def defaultconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()
        #convert datetime to readable

client = boto3.client('s3')
bucket_name = ""

parser = argparse.ArgumentParser(description="Arguments to supply bucket name for our s3 site") # ASK!WHY! THIS NO WORK
parser.add_argument('-s', '--sitename', dest='site_name', default='', type=str, help='enter a unique bucket name for s3 site')

args = parser.parse_args()
if not args.site_name:
    print(f"nothing said, so random it is")
    bucket_name += "".join(random.choices(string.ascii_lowercase, k=10))#adds a random 10 char to prev named bucket name (in var already)
else:
    print(f"you said a bucket name of {args.site_name}")
    bucket_name = args.site_name
try:
    bucket_response = client.create_bucket(Bucket = bucket_name)
    bucket_policy = { 
        'Version': '2012-10-17',
        'Statement': [{
            'Sid': 'AddPerm',
            'Effect': 'Allow',
            'Principal': '*',
            'Action': ['s3:GetObject'],
            'Resource': "arn:aws:s3:::%s/*" % bucket_name
        }]
    }
    bucket_policy_string = json.dumps(bucket_policy)

    response = client.put_bucket_policy(
        Bucket=bucket_name,
        Policy=bucket_policy_string
    )

    put_bucket_response = client.put_bucket_website( 
        Bucket=bucket_name, 
        WebsiteConfiguration={ 
            'ErrorDocument': {'Key': 'error.html'}, 
            'IndexDocument': {'Suffix': 'index.html'}, 
        } 
    )
    indexFile = open('index.html', 'rb')
    indexresponse = client.put_object(Body=indexFile,Bucket=bucket_name,Key='index.html',ContentType='text/html')
    indexFile.close()
    print(indexresponse)

    errorFile = open('error.html', 'rb')
    errorresponse = client.put_object(Body=errorFile,Bucket=bucket_name,Key='error.html',ContentType='text/html')
    errorFile.close()
    print(errorresponse)
except botocore.exceptions.ClientError as error:
    if error.response['Error']['Code'] == 'InvalidToken':
        print("you AWS credentials are invalid or out of date, new credentials can be entered with cmd aws config or changed in .aws/credentials\n session token")
    elif error.response['Error']['Code'] =='InvalidAccessKeyId':
        print("you AWS credentials are invalid or out of date, new credentials can be entered with cmd aws config or changed in .aws credentials\n access key")
    elif error.response['Error']['Code'] =='SignatureDoesNotMatch':
        print("you AWS credentials are invalid or out of date, new credentials can be entered with cmd aws config or changed in .aws credentials\n secret key")
    else:
        print(f"Some other error occurred{error}")
except client.exceptions.BucketAlreadyExists as err:#isn't working right no error
    print("Bucket {} already exists!".format(err.response['Error']['BucketName']))
    print('Re-run with different Name')