try:
  import unzip_requirements
except ImportError:
  pass

import json
import base64
import boto3
from requests_toolbelt.multipart import decoder
import requests

def hello(event, context):
    s3=boto3.client("s3")
    dynamodb =  boto3.resource('dynamodb')
    table = dynamodb.Table('Input_table')
    # ec2 = boto3.resource('ec2')
    print(event)
    file_content=event["body"]
    decode_content=base64.b64decode(file_content)
    print(decode_content)
    print(event['headers'])
    content_type=event["headers"]["content-type"]
    bucket=[]
    for part in decoder.MultipartDecoder(decode_content, content_type).parts:
        bucket.append(part.text)
    #print(bucket[0])
    #print(bucket[1])
    response = s3.generate_presigned_post(Bucket = 'fovus-input', Key = 'InputFile.txt', ExpiresIn = 3600 )
    
    with open('/tmp/hello.txt', 'w') as f:
        f.write(bucket[1])
    
    files = {'file': open('/tmp/hello.txt', 'rb')}
    r = requests.post(response['url'], data=response['fields'], files=files)
    
    dynamoDict={
        'id': 1,
        'input_text': bucket[0],
        'input_file_path': 'fovus-input/InputFile.txt'
    }
    table.put_item(Item=dynamoDict)
    # txt_data =  bucket[1].encode()
    # print(txt_data)      
    # s3_upload=s3.put_object(Bucket="fovus-input",Key="Inputfile.txt",Body=txt_data)

    # instances = ec2.create_instances(
    #      ImageId = 'ami-0be7e6029c6f1993b',
    #      MinCount = 1,
    #      MaxCount = 1,
    #      InstanceType = 't2.micro',
    #      KeyName = 'my_key_pair',
    #      SecurityGroupIds=['sg-0d65122ae2ea576ff'],
    #      TagSpecifications = [{'ResourceType': 'instance', 'Tags': [{'Key':'Instance', 'Value': 'Trigger_script'}]}]
    # )
    
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

def hello2(event, context):
    ec2 = boto3.resource('ec2')
    instances = ec2.create_instances(
         ImageId = 'ami-0be7e6029c6f1993b',
         MinCount = 1,
         MaxCount = 1,
         InstanceType = 't2.micro',
         KeyName = 'my_key_pair',
         SecurityGroupIds=['sg-0d65122ae2ea576ff'],
         TagSpecifications = [{'ResourceType': 'instance', 'Tags': [{'Key':'Instance', 'Value': 'Trigger_script'}]}]
    )