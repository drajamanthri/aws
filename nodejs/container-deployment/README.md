<h1>Lambda Container Deployment</h1>
<h2>Prerequisites</h2>
<ul>
    <li>AWS CLI</li>
    <li>Docker</li>
    <li>Python</li>
</ul>
<h2>Create Image</h2>
Create the project folder and change the directory into the project folder.<br>

Create a new Node.js project with npm. To accept the default options provided in the interactive experience, press Enter.<br>

<code>
npm init
</code>
<br>

Create a new file called index.js<br>
<code>
<pre>
exports.handler = async (event) => {
   console.log('hello from the container.')
};
</pre>
</code>
<br>

Create a new Dockerfile.<br>
<code>
<pre>
FROM public.ecr.aws/lambda/nodejs:16.2023.11.18.13
COPY index.js ${LAMBDA_TASK_ROOT}/
CMD [ "index.handler" ]
</pre>
</code>
<br>

Build the docker image<br>
<code>
docker build --platform linux/amd64 -t docker-image:test .
</code>
<br>
docker-image: this is the image name<br>
test: this is the tag<br>

<h2>Deploy Image</h2>
Login to AWS Console.<br>
Create an ECR repository. Lets call it test-repo.<br>
Login to ECR<br>

<code>
aws ecr get-login-password --region us-west-1 | docker login --username AWS --password-stdin account_id.dkr.ecr.us-west-1.amazonaws.com
</code>
<br>
replace account_id with the actual account id.<br>
Set the –region value to the desired region.<br>
<br>
Run the docker tag command to tag your local image into your Amazon ECR repository as the latest version.<br>

<code>
docker tag docker-image:test account_id.dkr.ecr.us-west-1.amazonaws.com/test-repo:latest
</code>
<br>
‘account_id.dkr.ecr.us-west-1.amazonaws.com/test-repo’ is the URI of the repository. <br>

Push the image<br>
<code>
docker push account_id.dkr.ecr.us-west-1.amazonaws.com/test-repo:latest
</code>

<h2>Create Lambda</h2>
Create a Lambda function by an image. <br>
Choose previously created ECR images. <br>

Run the lambda function and check if the message printed by the handler function appears in CloudWatch. The function execution role should have permissions to access CloudWatch logs.
