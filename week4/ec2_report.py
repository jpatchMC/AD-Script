#!/usr/bin/env python3
from http.client import responses
from imghdr import what
from multiprocessing.sharedctypes import Value
from tokenize import Name
import boto3, csv


def Get_Instances():
    Name = input("Define Name: ")
    what = input("define Value : ")
    ec2_client=boto3.client('ec2')
    #return ec2_client.describe_instances() 1st part version, werks fine but what if lot of stuff
    paginator = ec2_client.get_paginator('describe_instances')
    page_list = paginator.paginate(
        Filters=[
            {
                'Name': Name,
                'Values': [what],
                
                #'Name': 'root-device-type', misunderstood
                #'Values': [
                #    'ebs',
                #]
            }
        ]    
    )
    response = [] #just makin this a list
    for page in page_list:
        for reservation in page['Reservations']:
            response.append(reservation)
    return response


def CSV_Writer(header , content):
    hfile = open('export.csv', 'w')
    writer = csv.DictWriter(hfile, fieldnames=header)
    writer.writeheader()
    for line in content:
        writer.writerow(line)
    hfile.close()
def main():
    response = Get_Instances()
    headerRow = ['InstanceId','InstanceType','State', 'PublicIpAddress','Monitoring'] #,'RootDeviceType']
    content = []
    for instance in response:
       for ec2 in instance['Instances']:
        #print (ec2['InstanceId'])
            content.append(
                    {
                        "InstanceId" : ec2['InstanceId'],
                        "InstanceType" :ec2['InstanceType'],
                        "State" : ec2['State']['Name'],
                        #"PublicIpAddress": ec2['PublicIpAddress'],#won't cover null
                        "PublicIpAddress": ec2.get('PublicIpAddress',"N/A"),#n/a as a value for undifined/null. though with the filter in paginator this isn't needed because it will throw anything but running instances out
                        "Monitoring" : ec2['Monitoring']['State'],
                        #"RootDeviceType" : ec2['RootDeviceType']
                    }
            )
    print(content)
    CSV_Writer(headerRow,content)#write to function
    #print(Get_Instances())

if __name__ == "__main__":
    main()