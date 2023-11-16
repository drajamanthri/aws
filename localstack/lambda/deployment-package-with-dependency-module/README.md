<h1>Deployment Package with Dependency Module (Layer Workaround)</h1>
<p>
In localstack, lambda layers are supported only in the pro version. The workaround is to include the dependencies  alongside the function code. This is possible because the localstack does not limit file upload size.
</p>


<h2>Dependencies</h2>
<p>
Create a file called hello_layer.py and add the module code on it.
</p>
<p>hello_layer.py</p>
<code>
<pre>
def util():
  print('Hello from the layer')
</pre>
</code>


<h2>Function Code File</h2>
<p>
Create the function code file in the folder.
</p>
<p>hello.py</p>
<code>
<pre>
def handler(event, context):
  #import the layer and call a function defined in the layer.
  import hello_layer
  hello_layer.util()


  print('hello')
  return 'hello'
</pre>
</code>

<h2>Create Zip Package</h2>
<p>
Lambda expects your source code and its dependencies all to be at the root of the .zip file. Create the zip file as follows.
</p>
<p>hello.py</p>
<code>
<pre>
zip -r package.zip .
</pre>
</code>

<h2>Create lambda Function</h2>
<p>
Create the lambda function with the zip file that contain the function and dependent module code
</p>

<code>
<pre>
awslocal lambda create-function \
    --function-name hello \
    --runtime python3.8 \
    --zip-file fileb://package.zip \
    --handler hello.handler \
    --role arn:aws:iam::000000000000:role/lambda-role

</pre>
</code>

<h2>Invoke the lambda function with output file</h2>


<code>
<pre>
awslocal lambda invoke --function-name hello  output.txt

</pre>
</code>

Check the logs to see if the module logs are present. 