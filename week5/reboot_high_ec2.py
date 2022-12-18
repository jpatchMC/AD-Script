#!/usr/bin/env python3
import ec2,sns
import boto3

DRYRUN = False

sts_client = boto3.client("sts")
account_id = sts_client.get_caller_identity()["Account"]

ec2_client = boto3.client('ec2')
image_ID = ec2.Get_Image(ec2_client)

instance_ID = ec2.Create_EC2(ec2_client, image_ID)

print (f"Instance ID : {instance_ID}")

cw_client = boto3.client('cloudwatch')

sns_topic = sns.CreateSNSTopic("high-notification")
response = sns.SubscribeEmail(sns_topic, 'jpatch@madisoncollege.edu')

response = cw_client.put_metric_alarm(
    AlarmName='Web_Server_HIGH_CPU_Utilization',
    ComparisonOperator='GreaterThanThreshold',
    EvaluationPeriods=2,
    MetricName='CPUUtilization',
    Namespace='AWS/EC2',
    Period=300,
    Statistic='Average',
    Threshold=80.0,
    ActionsEnabled=True,
    AlarmActions=[
        f'arn:aws:swf:us-east-1:{account_id}:action/actions/AWS_EC2.InstanceId.Reboot/1.0',
        f'arn:aws:sns:us-east-1:{account_id}:high-notification'
    ],
    AlarmDescription='Alarm when server CPU is greater than 80%',
    Dimensions=[
        {
            'Name': 'InstanceId',
            'Value': instance_ID
        },
    ]

)
