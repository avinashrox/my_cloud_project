# This is the code which runs inside the created ec2 instance. Only for reference purposes.

import boto3
from boto3.dynamodb.conditions import Key
s3 = boto3.client("s3")
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Input_table')
table2 = dynamodb.Table('Output_table')
response = table.get_item(
    Key={
        'id': 1
    }
)
print(response['Item']['input_text'])
s3.download_file(Bucket='fovus-input', Key='InputFile.txt', Filename= 'hello.txt')
with open('hello.txt',"r") as f:
    contents = f.read()
content2=contents+":"+response['Item']['input_text']   
print(content2) 
with open("OutputFile.txt","w") as f:
    f.write(content2)
s3.upload_file(Filename='OutputFile.txt', Bucket='fovus-input', Key='OutputFile.txt')    
dynamoDict={
        'id': 1,
        'output_file_path': 'fovus-input/OutputFile.txt'
    }
table2.put_item(Item=dynamoDict)