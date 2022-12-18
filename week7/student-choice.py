#!/usr/bin/env python3
import boto3
import argparse
#going to list policies that are customer (as oppesed to AWS) managed, reason being is you ay want to know who set the
#policy and if you should change it
client = boto3.client('iam')
parser = argparse.ArgumentParser(description="Arguments to figure out who made a policy")
parser.add_argument('-p', '--policy-scope', dest='policy_scope',default='All', type=str, help='search a policy manager: All | Local | AWS.')
args = parser.parse_args()
scope = args.policy_scope
response = client.list_policies(
    Scope=scope
)
#print(response)
for poli in response['Policies']:
    print(poli['PolicyName'])
    #for name in poli['PolicyName']:
        #print("y")


#for Polname in response['Policies'] 