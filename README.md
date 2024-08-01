
# Cloud Resume API Challenge

This is a project that deploys an AWS serverless API in conjunction with AWS lambda and Dynamo DB.this project was deployed with CICD pipeline using github actions and AWS CDK. the AWS CDK framework was written using Python.

## Architectural diagram
![project diagram](https://github.com/user-attachments/assets/9e94815c-42e0-4e54-b3fb-4941585be00e)

Prequistes
for the project creation to work seamlessly, ensure you have the following installed
1. NodeJS. this needs to be installed to allow the use of the AWS CDK framework.
2. AWS CDK. This is used when deploying the project resources to the AWS cloud.
3. AWS CLI
4. Python 3.9
5. Pip

##Infrastructure resources.
1. Lambda function. this is invoked from the API request which then retrieves JSON resume data from the Dynamo database.
2. API Gateway. it is provides the API, which is used to route HTTP requests to lambda for invocation, the API used was an HTTP API.
3. DynamoDB. it is the database service used to store the JSON resume data that is input.
4. IAM roles. these roles are to be assumed by services such as lambda to execute functions.
## Creation of the resources
The resources used were all created using infrastructure as code. ,y thought process was to first create all the resources using cloudformation and testing if a stack could be created in an AWS account. if creation is successful, you can now create python file for the stack to utilize AWS CDK.
set up CDK environment
to use AWS cdk download NodeJs to your local machine to allow you use CDK operations in the terminal in VS code. The CDK framework to be used uses python programming language.
```
npm install -g aws-cdk
```
if the terminal does not run the AWS CDK commands, run this command to get permission to run them.
```
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
```
create the resources template in a python file for the stack creation when deployed.

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```
make sure you have installed the CDK library for python such that the resources you create in the python file can be read during the deploy.
```
pip install aws-cdk-lib
```
you can utilize the use of CDK migrate command to streamline the files and dependencies used to make the CDK app. this command can be used after creating all the neccessary resources in Cloud formation.
```
cdk migrate --stack-name your_stack --from-path path/to/file.yaml --language python
```

## push your project files to Github
with the project files organised. you can then commit them to your github repo. make sure you have  VScode connected to your github account. commit the changes from the directory where the python file is created.
```
git init
git remote add origin htttps://repo url.git
git checkout b branch_name
git add .
git commit =m "deployment message"
```

## Github actions workflow
this is feature that enables your project have a CI/CD pipeline. You create a .yaml file in the action tab in your github account. The file is configured to run the deployment when the requests are made to your main branch or one of your choosing.
```
# This is a basic workflow to help you get started with Actions

name: Cloud Resume API DEPLOY

# Controls when the workflow will run
on:
  # Triggers the workflow on push or pull request events but only for the "main" branch
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

  # Allows you to run this workflow manually from the Actions tab
  workflow_dispatch:

# A workflow run is made up of one or more jobs that can run sequentially or in parallel
jobs:
  # This workflow contains a single job called "build"
  build:
    # The type of runner that the job will run on
    runs-on: ubuntu-latest

    # Steps represent a sequence of tasks that will be executed as part of the job
    steps:
      # Checks-out your repository under $GITHUB_WORKSPACE, so your job can access it
      - uses: actions/checkout@v4

      # Runs a single command using the runners shell
      - name: Configure AWS Credentials
        uses: aws-actions/configure-aws-credentials@v1
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_ACCESS_KEY }}
          aws-region: us-east-1
          
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '20'

      - name: Install dependencies
        run: |
          python3 -m pip install --upgrade pip
          npm install -g aws-cdk
          pip3 install -r requirements.txt
      - name: Bootstrap CDK
        run: |
          cdk bootstrap aws://${{ secrets.AWS_ACCOUNT_ID }}/${{ env.AWS_REGION }}
      - name: CDK Deploy
        run: |
          cdk deploy --app-path "app.py" --require-approval never
      - name: CDK Destroy
        run: |
          cdk destroy --app-path "app.py" --force
      - name: Destroy CDK Toolkit stack
        run: |
          aws cloudformation delete-stack --stack-name CDKToolkit
```
when the workflow file is updated, it runs which will lead to deployment of the CDK application consisting of the AWS resources. the AWS_ACCESS_KEY, AWS_ACCESS_KEY_ID, AWS_ACCOUNT_ID and AWS_REGION variables are defined in the secrets an variables section in the settings tab. these variable allow the workflow to be deployed in a specific region, account and users. make sure you create a new IAM user that uses access keys and allow to be accessed using AWS CLI.
### Input the JSON data in the database
with the dynamoDB resource created, create an item with a partition key defined from the infrastructure as code. insert the json schema with your data in the "JSON view" of the attrubute creation.
![dynamodb insert](https://github.com/user-attachments/assets/b2c5e54d-2c9e-4b9d-9387-e991ee28e384)
then you create the item.
## API Endpoint
The API endpoint that triggers the lambda function to retrieve the json data can then be tested.
```
https://t7em9zzti0.execute-api.us-east-1.amazonaws.com/prod/Resumes
```

## Clean up 
To clean up the resources, run the github workflow file  with the destroy command which will delete the stack and the CDK toolkit stack which is also part of the deployment.
```
  - name: CDK Destroy
      run: |
        cdk destroy --app-path "app.py" --force
  - name: Destroy CDK Toolkit stack
      run: |
        aws cloudformation delete-stack --stack-name CDKToolkit
```
