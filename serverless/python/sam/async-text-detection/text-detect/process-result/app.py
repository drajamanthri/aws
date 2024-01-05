import os
import json
import boto3


def lambda_handler(event, context):

    job_id = json.loads(event["Records"][0]["Sns"]["Message"])["JobId"]

    words = get_words(job_id)

    print(words)


def get_words(job_id):
    textract = boto3.client("textract")

    words = []

    #get the first response with the job id and extract words of it
    response = textract.get_document_text_detection(JobId=job_id)
    get_words_from_response(response, words)

    #get next token
    nextToken = None
    if "NextToken" in response:
        nextToken = response["NextToken"]

    #extract words as long as there is a next token
    while nextToken:
        response = textract.get_document_text_detection(
            JobId=job_id, NextToken=nextToken
        )
        get_words_from_response(response, words)
        nextToken = None
        if "NextToken" in response:
            nextToken = response["NextToken"]

    
    return words

def get_words_from_response(response, words):
    for item in response["Blocks"]:
        if item["BlockType"] == "WORD":
            words.append({'Page':item['Page'], 'Text': item['Text']})

