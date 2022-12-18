#!/usr/bin/env python3
from sqlite3 import Date
from urllib import response
import boto3,datetime,pytz

IAMclient = boto3.client('iam')

def iamused():
    response = IAMclient.list_roles()
    #return response
    #[['RoleLastUsed']:{'LastUsedDate': datetime(2022, 7, 13)}]
    for Role in response['Roles']:
        #print (Role)
        if 'CreateDate' in Role.keys():
            #print(Role['CreateDate'])
            #print (Role)
            #for iamlastusd in Role['LastUsedDate']:
                #if 
                #return iamlastusd#WHYYYYYYYYY

            if Role['CreateDate'] >(pytz.utc.localize(datetime.datetime.utcnow())-datetime.timedelta(days=90)):
                print(f" new role made on: {Role['CreateDate']},{Role['RoleName']} is role's name")
                iam90 = (Role['CreateDate'],Role['RoleName'])
def lstpol():    
    Presponse = IAMclient.list_policies()
    #print(Presponse)
    for POL in Presponse['Policies']:
        if 'CreateDate' in POL.keys():
            if POL['CreateDate'] >(pytz.utc.localize(datetime.datetime.utcnow())-datetime.timedelta(days=90)):
                Poldate = str(POL['CreateDate'])
                print(f"new Policy was made on: {Poldate},{POL['PolicyName']} is the Policy name")





def main():
    print(iamused())
    print(lstpol())
if __name__=="__main__":
    main()