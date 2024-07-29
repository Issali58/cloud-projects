from aws_cdk import Stack
import aws_cdk as cdk
import aws_cdk.aws_apigatewayv2 as apigatewayv2
import aws_cdk.aws_dynamodb as dynamodb
import aws_cdk.aws_iam as iam
import aws_cdk.aws_lambda as aws_lambda
from constructs import Construct

"""
  CLOUD RESUME API WITH AWS STACK
"""
class CloudApIresumeChallengeStack(Stack):
  def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
    super().__init__(scope, construct_id, **kwargs)

    # Applying default props
    props = {
      'dynamoDBnames': kwargs.get('dynamoDBnames', 'Resumes'),
    }

    # Resources
    funcExecutionRole = iam.CfnRole(self, 'FuncExecutionRole',
          assume_role_policy_document = {
            'Statement': [
              {
                'Action': [
                  'sts:AssumeRole',
                ],
                'Effect': 'Allow',
                'Principal': {
                  'Service': [
                    'lambda.amazonaws.com',
                  ],
                },
              },
            ],
            'Version': '2012-10-17',
          },
          path = '/',
          policies = [
            {
              'policyName': 'AmazonDynamoDBReadOnlyAccess',
              'policyDocument': {
                'Version': '2012-10-17',
                'Statement': [
                  {
                    'Effect': 'Allow',
                    'Action': [
                      'dynamodb:List',
                      'dynamodb:GetItem',
                      'dynamodb:GetResourcePolicy',
                      'dynamodb:Query',
                      'dynamodb:Scan',
                      'dynamodb:PartiQLSelect',
                    ],
                    'Resource': f"""arn:aws:dynamodb:{self.region}:{self.account}:table/Resumes""",
                  },
                ],
              },
            },
          ],
        )

    myDynamoDBtable = dynamodb.CfnTable(self, 'MyDynamoDBtable',
          table_name = props['dynamoDBnames'],
          attribute_definitions = [
            {
              'attributeName': 'email',
              'attributeType': 'S',
            },
            {
              'attributeName': 'name',
              'attributeType': 'S',
            },
            {
              'attributeName': 'phone',
              'attributeType': 'S',
            },
            {
              'attributeName': 'address',
              'attributeType': 'S',
            },
          ],
          key_schema = [
            {
              'attributeName': 'email',
              'keyType': 'HASH',
            },
            {
              'attributeName': 'phone',
              'keyType': 'RANGE',
            },
          ],
          provisioned_throughput = {
            'readCapacityUnits': 5,
            'writeCapacityUnits': 5,
          },
          global_secondary_indexes = [
            {
              'indexName': 'Basics',
              'keySchema': [
                {
                  'attributeName': 'name',
                  'keyType': 'HASH',
                },
                {
                  'attributeName': 'phone',
                  'keyType': 'RANGE',
                },
              ],
              'projection': {
                'projectionType': 'ALL',
              },
              'provisionedThroughput': {
                'readCapacityUnits': 5,
                'writeCapacityUnits': 5,
              },
            },
            {
              'indexName': 'LocationIndex',
              'keySchema': [
                {
                  'attributeName': 'address',
                  'keyType': 'HASH',
                },
              ],
              'projection': {
                'projectionType': 'ALL',
              },
              'provisionedThroughput': {
                'readCapacityUnits': 5,
                'writeCapacityUnits': 5,
              },
            },
          ],
        )

    lambdafunction = aws_lambda.CfnFunction(self, 'lambdafunction',
          role = funcExecutionRole.attr_arn,
          handler = 'index.handler',
          runtime = 'python3.9',
          code = {
            'zipFile': 'import os\nimport json\nimport boto3\nfrom decimal import Decimal\n\ndynamodb = boto3.resource(\'dynamodb\')\ndef handler(event, context):\n    table_name = \'Resumes\'\n    table = dynamodb.Table(table_name)\n    headers = {\n        \"Content-Type\": \"application/json\"\n    }\n    try:\n        # Scan the table to retrieve all items\n        response = table.scan()\n        items = response[\'Items\']\n        \n        # Handle any additional pages of results\n        while \'LastEvaluatedKey\' in response:\n            response = table.scan(ExclusiveStartKey=response[\'LastEvaluatedKey\'])\n            items.extend(response[\'Items\'])\n        \n        return {\n            \'statusCode\': 200,\n            \'body\': json.dumps(items)\n        }\n    \n    except Exception as e:\n        return {\n            \'statusCode\': 500,\n            \'body\': json.dumps({\'error\': str(e)})\n        }\n',
          },
          environment = {
            'variables': {
              'table_name': props['dynamoDBnames'],
            },
          },
        )

    apigateway = apigatewayv2.CfnApi(self, 'apigateway',
          name = 'CloudResumeAPI',
          description = 'API for Cloud Resume Challenge',
          protocol_type = 'HTTP',
        )
    apigateway.add_dependency(lambdafunction)

    apiGatewayStage = apigatewayv2.CfnStage(self, 'ApiGatewayStage',
          api_id = apigateway.ref,
          stage_name = 'prod',
          auto_deploy = False,
        )

    lambdaPermission = aws_lambda.CfnPermission(self, 'LambdaPermission',
          function_name = lambdafunction.attr_arn,
          action = 'lambda:InvokeFunction',
          principal = 'apigateway.amazonaws.com',
          source_arn = ''.join([
            'arn:aws:execute-api:',
            self.region,
            ':',
            self.account,
            ':',
            apigateway.ref,
            '/*/*/Resumes',
          ]),
        )

    httpApiIntegration = apigatewayv2.CfnIntegration(self, 'httpApiIntegration',
          api_id = apigateway.ref,
          integration_type = 'AWS_PROXY',
          integration_uri = f"""arn:aws:apigateway:{self.region}:lambda:path/2015-03-31/functions/{lambdafunction.attr_arn}/invocations""",
          payload_format_version = '2.0',
          timeout_in_millis = 10000,
        )

    httpApiRoute = apigatewayv2.CfnRoute(self, 'HttpApiRoute',
          api_id = apigateway.ref,
          route_key = 'GET /Resumes',
          target = '/'.join([
            'integrations',
            httpApiIntegration.ref,
          ]),
        )

    # Outputs
    """
      http api endpoint url.
    """
    self.httpapiurl = ''.join([
      'https://',
      apigateway.ref,
      '.execute-api.',
      self.region,
      '.amazonaws.com/',
      apiGatewayStage.ref,
      '/',
    ])
    cdk.CfnOutput(self, 'CfnOutputhttpapiurl', 
      key = 'httpapiurl',
      description = 'http api endpoint url.',
      value = str(self.httpapiurl),
    )



