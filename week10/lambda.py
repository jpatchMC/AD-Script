from cgitb import handler
from urllib import response
import boto3
lambda_client = boto3.client('lambda')
iam = boto3.client('iam')

def Create_Lambda(function_name):
    role_response = iam.get_role(RoleName='LabRole')
    handler = open('lambda_stop_function.zip', 'rb')
    zipped_code = handler.read()

    response = lambda_client.create_function(
        FunctionName = function_name,
        Role = role_response['Role']['Arn'],
        Publish = True,
        PackageType = 'Zip',
        Runtime = 'python3.9',
        Code={
            'ZipFile': zipped_code  #its dic 
        },
        Handler = 'lambda_stop_function.lambda_handler' #which func for lambda file.def
    )

    #lambda_client = boto3.client('lambda')
def Invoke_Lambda(function_name):
    invoke_response = lambda_client.invoke(FunctionName = function_name)
    return invoke_response

def main():
    functionname = 'StopEC2'
    try:
        function = lambda_client.get_function(FunctionName=functionname)
        print ("Function present")
    except:
        print("creating function")
        response = Create_Lambda(functionname)
    print("Invoking Lambda Function")
    Invoke_Lambda(functionname)
if __name__== "__main__" :
    main()