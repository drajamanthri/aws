import os
import json
import boto3
from urllib.parse import unquote_plus

OUTPUT_BUCKET_NAME = os.environ["OUTPUT_BUCKET_NAME"]
# OUTPUT_S3_PREFIX = os.environ["OUTPUT_S3_PREFIX"]
SNS_TOPIC_ARN = os.environ["SNS_TOPIC_ARN"]
TEXTRACT_ROLE_ARN = os.environ["TEXTRACT_ROLE_ARN"]


def lambda_handler(event, context):

    event_body = event['Records'][0]['body']
    event_body = json.loads(event_body)
    if 'bucket' not in event_body:
        print('The bucket is not in the sqs message')
        return
    
    if 'key' not in event_body:
        print('Ket is not in the SQS message')
        return
    
    #bucket = bucket name that triggered the event
    bucket = event_body['bucket']
    #key: test.docx
    key = event_body['key']
    print('src bucket', bucket, 'key', key)


    textract = boto3.client("textract")

    response = textract.start_document_text_detection(
        DocumentLocation={"S3Object": {"Bucket": bucket, "Name": key}},
        #OutputConfig={"S3Bucket": OUTPUT_BUCKET_NAME, "S3Prefix": OUTPUT_S3_PREFIX},
        OutputConfig={"S3Bucket": OUTPUT_BUCKET_NAME},
        NotificationChannel={"SNSTopicArn": SNS_TOPIC_ARN, "RoleArn": TEXTRACT_ROLE_ARN},
    )
    if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
        return {"statusCode": 200, "body": json.dumps("Job created successfully!")}
    else:
        return {"statusCode": 500, "body": json.dumps("Job creation failed!")}
