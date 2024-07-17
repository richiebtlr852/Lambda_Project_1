
# My ETL Project

## Overview
This project involves an AWS Lambda function that is triggered by an S3 event to copy files from a source S3 bucket to a target S3 bucket and write logs to CloudWatch.

## Setup Instructions

### AWS Infrastructure
1. **Create S3 Buckets**:
    - Source Bucket: `your-source-bucket-name`
    - Target Bucket: `your-target-bucket-name`

2. **Create Lambda Function**:
    - Create a new Lambda function in the AWS Console.
    - Configure the function to be triggered by the S3 event on the source bucket.
    - Set the necessary IAM roles and policies to allow the Lambda function to access the S3 buckets and CloudWatch logs.

3. **Set Environment Variables**:
    - If your Lambda function relies on environment variables, configure them in the AWS Lambda console.

### Deployment Instructions

1. **Install Dependencies**:
    ```sh
    pip install -r lambda/requirements.txt -t lambda/
    ```

2. **Package Lambda**:
    ```sh
    cd lambda
    zip -r9 ../lambda_function.zip .
    ```

3. **Deploy Lambda**:
    ```sh
    aws lambda update-function-code --function-name your_lambda_function_name --zip-file fileb://lambda_function.zip
    ```

## CI/CD Pipeline
The Jenkins pipeline is defined in the `Jenkinsfile` and includes steps for installing dependencies, packaging the Lambda function, and deploying it to AWS.