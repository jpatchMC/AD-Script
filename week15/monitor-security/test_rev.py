import boto3

ec2 = boto3.client('ec2')
closeresponse = ec2.revoke_security_group_ingress(
    GroupId='sg-07f4dc0d6046ee57f',
    IpPermissions=[
        {
            'FromPort': 22,
            'IpProtocol': 'tcp',
            'ToPort': 22,
            'IpRanges': [
                {
                    'CidrIp': '0.0.0.0/0',
                },
            ],
        },
    ]
)
print(closeresponse)