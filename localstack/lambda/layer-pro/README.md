<h1>Lambda layers</h1>
<p>
In aws lambda, function code upload size is limited to 50MB. But lambda layers provide additional space.
</p>
<p>
In localstack, lambda layers are supported only in the pro version. The workaround is to include the layer code alongside the function code. This is possible because the localstack does not limit file upload size.
</p>
<h3>
The following process only works in the pro version of localstack.
</h3>
<h2>Create layer file and zip file</h2>
<p>
create a folder called python and create the layer file in the python folder. This folder structure is required by aws. 
</p>
<p>python/hello_layer.py</p>
<code>
<pre>
def util():
  print('Hello from the layer')
</pre>
</code>
<p>Create the zip file.</p>
<code>
<pre>
zip -r hello_layer.zip python
</pre>
</code>

<h2>Publish Layer</h2>
<p>
Run following command on the terminal to publish lambda layer. 
</p>

<code>
<pre>
awslocal lambda publish-layer-version --layer-name hello_layer --zip-file fileb://hello_layer.zip
</pre>
</code>

<p>
Write down the layer version ARN which will look something like this.
</p>
<code>
<pre>
arn:aws:lambda:us-east-1:000000000000:layer:hello_layer:1
</pre>
</code>


<h2>Create lambda function file and zip</h2>
<p>
Add the following code in hello.py.
</p>

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

<p>create the zip file</p>
<code>
<pre>
zip hello.zip hello.py
</pre>
</code>

<h2>Create lambda Function With the Layer</h2>
<p>
Run the following command on the terminal to create the lambda function that uses the layer. 
</p>

<code>
<pre>
awslocal lambda create-function \
    --function-name hello \
    --runtime python3.8 \
    --zip-file fileb://hello.zip \
    --handler hello.handler \
    --role arn:aws:iam::000000000000:role/lambda-role \
    --layers arn:aws:lambda:us-east-1:000000000000:layer:hello_layer:1

</pre>
</code>

<h2>Invoke the lambda function with output file</h2>
<pre>
<code>
awslocal lambda invoke --function-name hello  output.txt
</pre>
</code>

<p>Check the docker logs to see if the message from the layer is printed</p>