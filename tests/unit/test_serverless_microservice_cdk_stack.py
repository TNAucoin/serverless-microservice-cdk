import aws_cdk as core
import aws_cdk.assertions as assertions

from serverless_microservice_cdk.serverless_microservice_cdk_stack import ServerlessMicroserviceCdkStack

# example tests. To run these tests, uncomment this file along with the example
# resource in serverless_microservice_cdk/serverless_microservice_cdk_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = ServerlessMicroserviceCdkStack(app, "serverless-microservice-cdk")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
