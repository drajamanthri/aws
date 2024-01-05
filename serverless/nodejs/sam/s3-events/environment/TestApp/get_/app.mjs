import { GetItemCommand, DynamoDBClient } from "@aws-sdk/client-dynamodb";

const client = new DynamoDBClient({ region: "us-west-1" });

 /**
 * This function is getting called by api.
 * https://0j1m0gwbj4.execute-api.us-west-1.amazonaws.com/Prod/get?id='file1.pdf'
 * id query param is required.
 * 
 * This function returns the record corresponding to the given id from TestAppFiles DynamoDb table.
 * 
 * Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format
 * @param {Object} event - API Gateway Lambda Proxy Input Format
 *
 * Context doc: https://docs.aws.amazon.com/lambda/latest/dg/nodejs-prog-model-context.html 
 * @param {Object} context
 *
 * Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
 * @returns {Object} object - API Gateway Lambda Proxy Output Format
 * 
 */

export const lambdaHandler = async (event, context) => {

    //curl https://0j1m0gwbj4.execute-api.us-west-1.amazonaws.com/Prod/get?id='file1.pdf'
    //curl http://127.0.0.1:3000/get?id='file1.pdf'
    // if ('queryStringParameters' in event && event.queryStringParameters != null) {

    let id = event['queryStringParameters']['id'];
    const command = new GetItemCommand({
        TableName: "TestAppFiles",

        Key: {
            id: { S: id },
        }
    });

    let response = await client.send(command);

    // let response = {
    //     '$metadata': {
    //         httpStatusCode: 200,
    //         requestId: 'KEMGS068254R4M4CH049SJ661FVV4KQNSO5AEMVJF66Q9ASUAAJG',
    //         extendedRequestId: undefined,
    //         cfId: undefined,
    //         attempts: 1,
    //         totalRetryDelay: 0
    //     },
    //     ConsumedCapacity: undefined,
    //     Item: {
    //         id: { S: 'file1.pdf' },
    //         timestamp: { S: '2023-07-22T04:58:37.588Z' }
    //     }
    // };

    
    if ('Item' in response) {
        
        return {
            "statusCode": 200,
            "body": JSON.stringify({
                "item": response.Item
            })
        }
        
    }

};
