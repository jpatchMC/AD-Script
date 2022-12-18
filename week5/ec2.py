#!/usr/bin/env python3
from urllib import response
import boto3
DRYRUN = False
client = boto3.client('ec2')

def Get_Image(ec2_client):
    IMresponse = client.describe_images(
    Filters=[
        {
            'Name': 'description',
            'Values': ['Amazon Linux 2 AMI*']
        },
        {
            'Name': 'architecture',
            'Values': ['x86_64']
        },
        {
            'Name': 'owner-alias',
            'Values': ['amazon']
        }

        ],
    )
    return IMresponse['Images'][0]['ImageId']


def Create_EC2(ec2_client, AMI): ###set name here somewhere
    response = ec2_client.run_instances(
    ImageId=AMI,
    InstanceType='t2.micro',
    MaxCount=1,
    MinCount=1,
    DryRun= DRYRUN,
    SecurityGroups=['WebSG'],
    UserData='''
            #!/bin/bash -ex
            # Updated to use Amazon Linux 2
            yum -y update
            yum -y install httpd php mysql php-mysql
            /usr/bin/systemctl enable httpd
            /usr/bin/systemctl start httpd
            cd /var/www/html
            wget https://aws-tc-largeobjects.s3-us-west-2.amazonaws.com/CUR-TF-100-ACCLFO-2/lab6-scaling/lab-app.zip
            unzip lab-app.zip -d /var/www/html/
            chown apache:root /var/www/html/rds.conf.php
            ''',
            
    )
    return response['Instances'][0]['InstanceId']

#def DISP (c2_client):
#ec2 = boto3.client('ec2')
#filters = [
#    {'Name': 'domain'}
#]
#response = ec2.describe_addresses(Filters=filters)
#print (response)

def main():    
    client = boto3.client('ec2')
    AMI = Get_Image(client)
    instID= Create_EC2(client, AMI)
    #print(response)
    ec2_instance = boto3.resource('ec2')
    ec2 = ec2_instance.Instance(instID)
    #print(ec2.instance_id)
    #print("wait for start up\n")
    print(f"{ec2.instance_id} {ec2.state['Name']}\n")
    
if __name__== "__main__" :
    main()