<h1>Trigger lambda function by s3 event.</h1>
<p>
In this example we are going to do the following exercise in localstack.
<ul>
    <li>1. Create a lambda function.</li>
    <li>2. Create a s3 bucket.</li>
    <li>3. Trigger the lambda function on s3 bucket object creation.</li>
</ul>
</p>


<h2>Create the function code</h2>
<p>
Create a python file called process.py with the following code. The name of the function which will get triggered by the s3 event is called "handler". And the function prints the bucket name and the key.
</p>
<code>
<pre>
def handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    print(bucket, key)
</pre>
</code>

<h2>Create the deployment package</h2>
<p>
Zip the process.py file to create the deployment package.
</p>
<code>
<pre>
zip process.zip process.py
</pre>
</code>


<h2>Create the lambda function</h2>
<p>
Create a lambda function called "process" by using the previously created zip file.
</p>
<code>
<pre>
awslocal lambda create-function \
    --function-name process \
    --runtime python3.8 \
    --zip-file fileb://process.zip \
    --handler process.handler \
    --role arn:aws:iam::000000000000:role/lambda-role
</pre>
</code>
<p>
Write down the generated function Arn.
</p>


<h2>Create the s3 bucket</h2>
<p>
Create a s3 bucket called file-bucket.
</p>
<code>
<pre>
awslocal s3 mb s3://file-bucket
</pre>
</code>


<h2>Register the lambda function as the s3 Object Create event handler</h2>
<p>
create s3-notif-config.json
</p>
<code>
<pre>
{
    "LambdaFunctionConfigurations": [
        {
            "Id": "s3eventtriggerslambda",
            "LambdaFunctionArn": "arn:aws:lambda:us-east-1:000000000000:function:process",
            "Events": ["s3:ObjectCreated:*"]
        }
    ]
}

</pre>
</code>
<p>
In this file set the function Arn with the correct arn written down in the previous step.
</p>
<p>
Run the following command to attach the notification configuration with the file-bucket.
</p>
<code>
<pre>
awslocal s3api put-bucket-notification-configuration --bucket file-bucket \
--notification-configuration file://s3-notif-config.json

</pre>
</code>
<h2>Test</h2>
<p>
Upload a file to the previously created s3 bucket called file-bucket and test if the lambda function logs the desired value.
</p>
<code>
<pre>
awslocal s3api put-object --bucket file-bucket \
--key upload-file1.txt --body=upload-file1.txt


</pre>
</code>