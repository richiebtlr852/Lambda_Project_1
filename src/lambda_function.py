"""
Lambda use case 1 - copy file from source s3 to target s3
"""

import json
import logging
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client('s3')

def lambda_handler(event, context):
    logger.info("Received event: " + json.dumps(event))
    
    for record in event['Records']:
        try:
            source_bucket = record['s3']['bucket']['name']
            source_key = record['s3']['object']['key']
            trg_bucket = 'lambda1-test-target'
            copy_source = {'Bucket': source_bucket, 'Key': source_key}
            
            logger.info(f"Copying file {source_key} from bucket {source_bucket} to bucket {trg_bucket}") 
            s3.copy_object(
                CopySource=copy_source, 
                Bucket=trg_bucket, 
                Key=source_key)
        
        except Exception as e:
            logger.error(f"Error copying the file {source_key} from bucket {source_bucket} to bucket {trg_bucket}: {e}")
            raise e
    
    return {
        'statusCode': 200,
        'body': json.dumps('File copied successfully, job well done!')
    }
