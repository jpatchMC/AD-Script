import boto3




#def attached_sgs(ec2):
def SGIDfromEC2(): #no args passed
    ec2 = boto3.client('ec2')
    SGIDs=[]
    EC2_response = ec2.describe_instances()
    for Reserv in EC2_response['Reservations']:
        for Inst in Reserv['Instances']:
                #print(Inst['InstanceId'])
            for SG in Inst['SecurityGroups']:
                    #print(SG)
                #print(f"AMIs of existing instances {Inst['InstanceId']} and their SecGroup name {SG['GroupName']}")
                SGIDs.append (SG['GroupId'])
    return SGIDs #this is outside fors because otherwise they stop when they hit it
def srchsg(SGIDs): #NEEDS SGID from above func here as its req for this to even work
    SGbad=[]
    ec2 = boto3.client('ec2') 
    SGsrch= ec2.describe_security_groups(GroupIds =SGIDs)    
    for securitygroups in SGsrch['SecurityGroups']:
        
        for permissions in securitygroups['IpPermissions']:
            #print(securitygroups)
            #print(permissions)
            if 'FromPort' in permissions: #fix error     
                if permissions['FromPort'] == 22:
                    for open_to in permissions['IpRanges']:
                        #print(open_to)
                        for ciderval in open_to.values():
                            if ciderval == '0.0.0.0/0':
                                #print(f"{securitygroups['GroupName']} attached to instanceID {Inst['InstanceId']} has an open port 22!")
                                #SGbad.append(securitygroups['GroupId'])
                                #for item in SGbad:
                                    closeresponse = ec2.revoke_security_group_ingress(
                                        GroupId=securitygroups['GroupId'],
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
                                    print(f"revokeing open port 22 on {securitygroups['GroupId']}")
                            if ciderval != '0.0.0.0/0':
                                print(f"While SSH is set on {securitygroups['GroupName']} it isn't open")
                #if permissions['FromPort'] != 22:
                    #print(f"no SSH permissions set for {securitygroups['GroupName']}")
        else:
            print(f"no ingress permissions set for {securitygroups['GroupName']}")
def main():
    mSGIDs = SGIDfromEC2() #need to set as veri to pass into other func
    #print(mSGID)
    srchsg(mSGIDs) #pass similar (to stand alone func) vari because of scope


if __name__ =="__main__":
    main()