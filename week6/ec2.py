#!/usr/bin/env python3
from urllib import response
import boto3,botocore
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
    try:   
        client = boto3.client('ec2')
        AMI = Get_Image(client)
        instID= Create_EC2(client, AMI)
        #print(response)
        ec2_instance = boto3.resource('ec2')
        ec2 = ec2_instance.Instance(instID)
        #print(ec2.instance_id)
        print("wait for start up\n")
        print(f"{ec2.instance_id} {ec2.state['Name']}\n")
        ec2.wait_until_running()
        print(f"{ec2.instance_id} {ec2.state['Name']}\n")
        ec2ip = boto3.client('ec2')##############wtf!#
    #    ipinstance = ec2ip.instance(ec2)
        ipresponse = ec2.public_ip_address
        print (f"Pulic ip: {ipresponse} \n")
        ec2tag = ec2.tags
        print(f"tag: {ec2tag} \n")
        tag = ec2.create_tags(
        DryRun=DRYRUN,
        Tags=[
            {
                    'Key': 'Name',
                'Value': 'Josh'
                },
        ]
        )
    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == 'UnauthorizedOperation':
            print("you likely have the region set wrong, check .aws/config")
        elif error.response['Error']['Code'] == 'AuthFailure':
            print('there is an issue with credentials, check .aws/credentials')
        elif error.response['Error']['Code'] == 'InvalidAMIID.Malformed'or'InvalidAMIID.NotFound':
            print("trying to use an incorrect AMI, check at both variables")
        else:
            print(f"Some other error occurred{error}")
    #except botocore.exceptions.ClientError as error:
        

if __name__== "__main__" :
    main()