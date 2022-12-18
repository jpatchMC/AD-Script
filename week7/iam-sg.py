#!/usr/bin/env python3
import boto3
import argparse
import ipaddress

from certifi import where
from click import secho

client = boto3.client('ec2')

parser = argparse.ArgumentParser(
    description="Arguments to supply Security Grouop name id applicable")
parser.add_argument('-s', '--security-group', dest='security_group',
                    default='', type=str, help='seach a specific SG-group or leave blank')
# [{'FromPort': 80 or 443, 'IpProtocol': 'tcp', 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
#response = client.describe_security_groups(GroupNames =['poop']  )
# for secgrp in response['SecurityGroups']:
# print(secgrp)
# print(secgrp['GroupName'])
# for allow in secgrp['IpPermissions'],['IpRanges'],[{'CidrIp': '0.0.0.0/0'}]:
# print(allow)
# for specific in allow:
# print(specific)
# if specific == {'CidrIp': '0.0.0.0/0'}:
# print(specific)
# for Cidr in specific['CidrIp']:
#Cidr = []
# print(type(Cidr))
# print(Cidr)
# if allow['IpRanges']['CidrIp'] == [0.0.0.0/0]:Cidr['IpRanges']
# print(response['GroupName'])

# print(response)


args = parser.parse_args()
if not args.security_group:
    print(f"searching all known SGs")
    response = client.describe_security_groups()
    wutip = {'CidrIp': '0.0.0.0/0'}
    #print(f"these group are in the search{response['GroupName']}")
    for secgrp in response['SecurityGroups']:
        # print(secgrp)
        # print(secgrp['GroupName'])
        # ,['IpRanges'],[{'CidrIp': '0.0.0.0/0'}]:
        for allow in secgrp['IpPermissions']:
            # print(allow.values())
            # if allow.values() == [{'CidrIp': '0.0.0.0/0'}]:
            # print("bad") dosen't work here
            for cidrdic in allow['IpRanges']:
                #print(cidrdic)
                #print(cidrdic.values())
                for cidrval in cidrdic.values():
                    #print(cidrval)
                    if cidrval == '0.0.0.0/0':
                        print(f"{secgrp['GroupName']} is open to the public internet on port {allow['FromPort']} using {allow['IpProtocol']}!")
                    if cidrval != '0.0.0.0/0': #wanted to make some clairity
                        print(f"{secgrp['GroupName']} has a specific IP {cidrval} set {allow['FromPort']} using {allow['IpProtocol']}")
                    #holy shiz finally! although i'm concerned that i am looking up the wrong set of rules, should it be egress???
                


else:  # this is so wrong it works but not really
    print(f'checking SG of {args.security_group} if nothing returns no rules set')
    SGname = args.security_group
    response = client.describe_security_groups(GroupNames=[SGname])
    for secgrp in response['SecurityGroups']:
        # print(secgrp)
        # print(secgrp['GroupName'])
        # print(secgrp['IpPermissions'])
       for allow in secgrp['IpPermissions']:
            #print(allow)
            # if allow.values() == [{'CidrIp': '0.0.0.0/0'}]:
            # print("bad") dosen't work here
            for cidrdic in allow['IpRanges']:
                    #print(cidrdic)
                    #print(cidrdic.values())
                for cidrval in cidrdic.values():
                    if cidrval == '0.0.0.0/0':
                        print(f"{secgrp['GroupName']} is open to the public internet on port {allow['FromPort']} using {allow['IpProtocol']}!")
                    if cidrval != '0.0.0.0/0':
                        print(f"{secgrp['GroupName']} seems to not be open because the IP is specific.")
                                
        