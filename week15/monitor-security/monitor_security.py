import boto3
"""
5.	In your script use boto3, find a function that lists all EC2 instances and get the security groups of each instance.
6.	Check each security group to ensure that port 22 is not open.
7.	If port 22 is open, use the revoke_security_group_ingress() function to remove access to port 22.
8.	Be sure to have print statements that explain what is happening (i.e.: name of the security group, whether or not port 22 is open, message when you close a port successfully, etc.)  You want to be sure the users of your script know what is happening.
"""
SGID=[]
SGbad=[]
ec2 = boto3.client('ec2')
#def attached_sgs(ec2):
EC2_response = ec2.describe_instances()
for Reserv in EC2_response['Reservations']:
    for Inst in Reserv['Instances']:
            #print(Inst['InstanceId'])
        for SG in Inst['SecurityGroups']:
                #print(SG)
            #print(f"AMIs of existing instances {Inst['InstanceId']} and their SecGroup name {SG['GroupName']}")
            SGID.append (SG['GroupId'])
#print( SGID)
SGsrch= ec2.describe_security_groups(GroupIds =SGID)    
#print(SGsrch)
for securitygroups in SGsrch['SecurityGroups']:
    #print(securitygroups)
    for permissions in securitygroups['IpPermissions']:
        #print(permissions)        
        if permissions['FromPort'] == 22:
           for open_to in permissions['IpRanges']:
            #print(open_to)
            for ciderval in open_to.values():
                if ciderval == '0.0.0.0/0':
                    print(f"{securitygroups['GroupName']} attached to instanceID {Inst['InstanceId']} has an open port 22!")
                    SGbad.append(securitygroups['GroupId'])
                    for item in SGbad:
                        closeresponse = ec2.revoke_security_group_ingress(
                            GroupId=item,
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
                        print(f"revokeing open port 22 on {item}")
                if ciderval != '0.0.0.0/0':
                    print(f"While SSH is set on {securitygroups['GroupName']} it isn't open")
        if permissions['FromPort'] != 22:
            print(f"no SSH permissions set for {securitygroups['GroupName']}")
        else:
            print(f"no ingress permissions set for {securitygroups['GroupName']}")