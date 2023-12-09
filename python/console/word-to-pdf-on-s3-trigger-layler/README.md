<h1>Word to Pdf on S3 Event</h1>
<h2>System Design</h2>
In this project we are going to convert a word file to pdf on upload to s3.
<img src='system_design.png'/>
<h2>Lambda function</h2>
See the lambda_function.py.
<h2>Install dependencies</h2>
<p>We are going to deploy dependencies as a lambda layer.
In the project folder create a folder called ‘python’ and install the dependencies in the python folder. Lambda requires the python dependencies in the ‘python’ folder. 
</p>
<p>
Libreoffice package works with python 3.8. Therefore we need to install dependencies for python 3.8.
</p>
<p>
If the dependency layer has platform compatibility issues, generate the dependencies on Amazon Linux 2 Cloud9 instance.
</p>
<p>
install aws python sdk
</p>
<code>
<pre>
pip3 install \
--target=python \
--implementation cp \
--python-version 3.8 \
--only-binary=:all: --upgrade \
boto3

</pre>
</code>

<p>install brotlipy used to extract the libreoffice package.</p>
<code>
<pre>
pip3 install \
--target=python \
--implementation cp \
--python-version 3.8 \
--only-binary=:all: --upgrade \
brotlipy

</pre>
</code>
<h2>Generate dependency layer and function zip files</h2>
<code>
<pre>
zip -r layer.zip python

zip fn.zip lambda_function.py
</pre>
</code>
<h2>Libreoffice layer</h2>
<p>
Option1: using prebuilt layer <br/>
Option2: download the lo.tar.br from the following link and create a zip file to create a layer. 
</p>
<code>
<pre>
https://github.com/vladholubiev/serverless-libreoffice/releases/tag/v6.4.0.1
https://medium.com/analytics-vidhya/convert-word-to-pdf-using-aws-lambda-cb111be0d685
</pre>
</code>
<h2>AWS Configurations</h2>
<h3>S3</h3>
<p>
Create the doc_bucket.<br/>
Create the pdf_bucket.
</p>
<h3>Lambda configurations</h3>
<p>
Create the lambda function.
</p>
<h4>Execution role</h4>
<p>Lambda function’s execution role should have read access to the doc_bucket and write access to the pdf_bucket. Or it can have full s3 access.</p>
<h4>S3 Trigger</h4>
<p>Add a lambda trigger where the source is the doc_bucket and the destination is the lambda function. </p>
<h4>Timeout</h4>
<p><pre>With 4GB memory, 
Exe time with cold start time: 12 sec
Exe time with warm start: 2 sec
Therefore 1 min of timeout should be sufficient.
</pre>
</p>
<h4>Memory</h4>
<p>Office extraction is done in memory. Office package size is 370 Mb. Therefore,
the memory has to be > 512 MB. When increasing memory, execution time
improved until 4GB. After that no improvement. Therefore, set the memory
to 4GB.
</p>
<h4>Provisioned concurrency</h4>
<p>Provision at least one instance to achieve a warm start. With provisioned
concurrency, we can eliminate the libreoffice extraction for the requests
after the first request.
</p>
<h2>Test</h2>
<p>Upload a doc file to the doc_bucket and check if the pdf file appears in the pdf_bucket.</p>
