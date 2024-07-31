
# Cloud Resume API Challenge

This is a project that deploys an AWS serverless API in conjunction with AWS lambda and Dynamo DB.this project was deployed with CICD pipeline using github actions and AWS CDK. the AWS CDK framework was written using Python.

## Architectural diagram
![project diagram](https://github.com/user-attachments/assets/9e94815c-42e0-4e54-b3fb-4941585be00e)

Prequistes
for the project creation to work seamlessly, ensure you have the following installed
1. NodeJS. this needs to be installed to allow the use of the AWS CDK framework.
2. AWS CDK. This is used when deploying the project resources to the AWS cloud.
3. Python 3.9
4. Pip

Infrastructure resources.
1. Lambda function. this is invoked from the API request which then retrieves JSON resume data from the Dynamo database.
2. API Gateway. it is provides the API, which is used to route HTTP requests to lambda for invocation, 

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the `.venv`
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.



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

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

