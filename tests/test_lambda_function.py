import json
import boto3
from moto import mock_s3
import lambda_function

@mock_s3
def test_lambda_handler():
    # Setup
    s3 = boto3.client('s3', region_name='us-east-1')
    source_bucket = 'source-bucket'
    target_bucket = 'richiebtlr-test-target'
    source_key = 'test.txt'
    s3.create_bucket(Bucket=source_bucket)
    s3.create_bucket(Bucket=target_bucket)
    s3.put_object(Bucket=source_bucket, Key=source_key, Body='Test content')

    event = {
        "Records": [
            {
                "s3": {
                    "bucket": {
                        "name": source_bucket
                    },
                    "object": {
                        "key": source_key
                    }
                }
            }
        ]
    }

    # Execute
    result = lambda_function.lambda_handler(event, None)

    # Verify
    copied_object = s3.get_object(Bucket=target_bucket, Key=source_key)
    copied_content = copied_object['Body'].read().decode('utf-8')

    assert result['statusCode'] == 200
    assert json.loads(result['body']) == 'File copied successfully'
    assert copied_content == 'Test content'