import pulumi
import pulumi_aws as aws

# size = "t2.micro"
# vpcid = "vpc-03e614bd20d610cc3"




lambda_role = aws.iam.Role("SulavlambdaRole",
    assume_role_policy="""{
        "Version": "2012-10-17",
        "Statement": [{
            "Action": "sts:AssumeRole",
            "Effect": "Allow",
            "Principal": {
                "Service": "lambda.amazonaws.com"
            }
        }]
    }"""
)
# Attach the AWS Lambda Basic Execution Role policy to the role.
lambda_exec_policy_attachment = aws.iam.RolePolicyAttachment("lambdaExecPolicyAttachment",
    policy_arn="arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole",
    role=lambda_role.name
)

lambda_function = aws.lambda_.Function(
    "Sulav-lambda",
    runtime="python3.9",
    # Use the ARN of the IAM Role
    role=lambda_role.arn, 
    code=pulumi.FileArchive("./lamdaFunction/lamdafunction.zip"),
    handler="lambda_function.my_handler",
    tags={
        "Name": "Sulav-lambda",
        "Creator": "Sulav",
        "Project": "Intern",
        "Deletable": "yes"
    }
)

# Create a new Lambda Function URL
lambda_function_url = aws.lambda_.FunctionUrl(
    "Sulav-lambda-url",
    function_name=lambda_function.name,
    authorization_type="NONE"
)

pulumi.export('lambda_function_arn', lambda_function.arn)
pulumi.export("lambda_function_url", lambda_function_url.function_url)