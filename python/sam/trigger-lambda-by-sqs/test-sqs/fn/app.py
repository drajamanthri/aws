import json


def lambda_handler(event, context):
    print(event['Records'][0]['body'])

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": event['Records'][0]['body'],
            }
        ),
    }
