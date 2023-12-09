<h1>Lambda Container Deployment</h1>
<h2>Prerequisites</h2>
<ul>
    <li>AWS CLI</li>
    <li>Docker</li>
    <li>Python</li>
</ul>
<h2>Creating an image from a base image</h2>
Create a directory for the project. And change into it.<br>
Create a file called lambda_function.py<br>

<code>
<pre>
import sys
def handler(event, context):
    return 'Hello from AWS Lambda using Python' + sys.version + '!'

</pre>
</code>

Create the file requirements.txt. This file should have all the dependencies. For example, if you use AWS SDK for python (boto3), it should contain boto3.<br>

<code>
boto3
</code>

Create a new Dockerfile in the project folder with the following configurations.<br>

<i>Dockerfile</i>
<code>
<pre>
FROM public.ecr.aws/lambda/python:3.11

# Copy requirements.txt
COPY requirements.txt ${LAMBDA_TASK_ROOT}

# Install the specified packages
RUN pip install -r requirements.txt

# Copy function code
COPY lambda_function.py ${LAMBDA_TASK_ROOT}

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "lambda_function.handler" ]

</pre>
</code>

<b>FROM:</b>  the URI of the base image<br>
<b>COPY:</b> copy the function code and runtime dependencies to {LAMBDA_TASK_ROOT}.<br>
<b>CMD:</b> the Lambda function handler.<br>

Build the docker image.<br>

<code>
docker build --platform linux/amd64 -t docker-image:test .
</code>

<b>linux/amd64:</b> build for linux amd64 <br>
<b>linux/arm64:</b> build for linux arm64 <br>
<b>docker-image:</b> this is the image name <br>
<b>test:</b> this is the given tag <br>

<h2>Test the image locally</h2>
build a docker image for the local environment. <br>

<code>
docker build -t docker-image:test .
</code>

Run the image<br>
<code>
docker run -p 9000:8080 docker-image:test
</code>

<b>9000:8080<b>: This binds port 8080 of the container to 9000 of the host machine.<br>
<b>docker-image<b>: the name of the image<br>
<b>test<b>: this is a image tag<br>

This command runs the image as a container and creates a local endpoint at<br>
<code>localhost:9000/2015-03-31/functions/function/invocations</code>

Call the endpoint from a new terminal window.<br>
<code>
curl "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{}'
</code>

invoke with payload<br>

<code>
curl "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{"payload":"hello world!"}'
</code>

The following command can be used to get the container id
<code>
docker ps
</code>

Stop the container as follows<br>
<code>
docker kill container_id
</code>
<h2>Deploy the image</h2>
If you haven’t built the deployment image, build the image.<br>
<code>
docker build --platform linux/amd64 -t docker-image:test .
</code>

Login to AWS console and create a Elastic Container Registry (ECR) repository. Lets call it test-repo.<br>
Copy the repository uri. <br>
Example <br>
<code>
1234.dkr.ecr.us-west-1.amazonaws.com/test-repo
</code>

Run the get-login-password command to authenticate the Docker CLI to your Amazon ECR registry. Without authenticating the docker commands will not work.<br>

<code>
aws ecr get-login-password --region us-west-1 | docker login --username AWS --password-stdin <aws-account-id>.dkr.ecr.us-west-1.amazonaws.com
</code>

Run the docker tag command to tag your local image into your Amazon ECR repository as the latest version.<br>

<code>
docker tag docker-image:test <ECRrepositoryUri>:latest
</code>

Run the docker push command to deploy your local image to the Amazon ECR repository. Make sure to include :latest at the end of the repository URI.<br>

<code>
docker push <aws-account-id>.dkr.ecr.us-west-1.amazonaws.com/test-repo:latest
</code>

<h2>Create lambda function</h2>
On the AWS Console, create an execution role for lambda.<br>
Create a lambda function. Let's call it test-lambda.<br>
Select container image option. Use the latest image of the previously created ECR repository. <br>
Select the previously created execution role.<br>

Test the function and observe the logs added by the function appear. <br>
