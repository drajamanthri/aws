<h1>Hello World</h1>
<p>
In this example we are going to see how to create a lambda function and invoke in localstack.
</p>
<h2>Create Python File</h2>
<p>
Create a python file called hello.py and add the following code. This file contain the code for the lambda file.
</p>
<code>
<pre>
def handler(event, context):
    print('hello')
    return 'hello'
</pre>
</code>

<h2>Create zip file</h2>
<p>
Create the deployment package by zipping the python file.
</p>
<code>
<pre>
zip hello.zip hello.py
</pre>
</code>

<h2>Create Lambda Function</h2>
<p>
Create a lambda function called hello on localstack.
</p>
<code>
<pre>
awslocal lambda create-function \
    --function-name hello \
    --runtime python3.8 \
    --zip-file fileb://hello.zip \
    --handler hello.handler \
    --role arn:aws:iam::000000000000:role/lambda-role

</pre>
</code>
<p>Check if the function has been created by using the following command</p>
<code>
<pre>
awslocal lambda list-functions

</pre>
</code>

<h2>Invoke Lambda Function</h2>
<p>
Invoke the lambda function by the following cli command.
</p>
<code>
<pre>
awslocal lambda invoke --function-name hello  output.txt

</pre>
</code>

<p>The output.txt should have the return value of the function.
The message ‘Hello’ will be printed on the docker localstack log. Make sure localstak DEBUG=1.
</p>

<h2>Trigger the lambda function by using url</h2>
<p>
Alternatively we can create a url to the lambda function and trigger by cURL.
</p>
<p>create a url</p>
<code>
<pre>
awslocal lambda create-function-url-config \
    --function-name hello \
    --auth-type NONE


</pre>
</code>

<p>The output.txt should have the return value of the function.
The message ‘Hello’ will be printed on the docker localstack log. Make sure localstak DEBUG=1.
</p>

<p>
copy the function url which will look something like this.

<code>
http://nkc25wlie5hfo0kg7aabcwqdi15a6a5h.lambda-url.us-east-1.localhost.localstack.cloud:4566/
</code>

</p>
<p>
Then trigger the function by curl.
</p>
<code>
curl -X POST \
'http://nkc25wlie5hfo0kg7aabcwqdi15a6a5h.lambda-url.us-east-1.localhost.localstack.cloud:4566/'

</code>