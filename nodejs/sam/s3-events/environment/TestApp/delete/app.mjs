import { DeleteItemCommand, DynamoDBClient } from "@aws-sdk/client-dynamodb";

const client = new DynamoDBClient({ region: "us-west-1" });

 /**
 * This function is getting called when an object is deleted from the testapp-files S3 bucket. 
 * Then this function deletes the object key from the TestAppFiles DynamoDb table.
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

    //on s3 object is deleted event
    //ObjectRemoved:Delete
    let s3ObjectKey = event.Records[0].s3.object.key;

    //object is created in s3
    //read s3 object key and timestamp from the s3 event and write it to DynamoDB
    //reference: https://docs.aws.amazon.com/sdk-for-javascript/v3/developer-guide/dynamodb-example-table-read-write.html
    
    const command = new DeleteItemCommand({
        TableName: "TestAppFiles",
        Key: {
            id: { S: s3ObjectKey },
        },
    });

    const response = await client.send(command);
    return response

};
