import aws_cdk as core
import aws_cdk.assertions as assertions

from active_directory_cdk.active_directory_cdk_stack import ActiveDirectoryCdkStack

# example tests. To run these tests, uncomment this file along with the example
# resource in active_directory_cdk/active_directory_cdk_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = ActiveDirectoryCdkStack(app, "active-directory-cdk")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
