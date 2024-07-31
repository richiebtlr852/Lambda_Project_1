"""
Lambda use case 1 - copy file from source s3 to target s3
"""

import json
import logging
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client('s3')

def get_config(bucket_name, config_key):
    try:
        response = s3.get_object(Bucket=bucket_name, Key=config_key)
        config_content = response['Body'].read().decode('utf-8')
        config = json.loads(config_content)
        return config
    except Exception as e:
        logger.error(f'Error reading config file from bucket {bucket_name} with key {config_key}: {e}')
        raise e
    

def lambda_handler(event, context):
    logger.info("Received event: " + json.dumps(event))

    # configuration file details
    config_bucket = 'lambda1-test-config'
    config_key = 'config.json'

    # fetch configuration data within config file
    config = get_config(config_bucket,config_key)
    trg_bucket = config['target_bucket']
    metadata_filename = config['metadata_filename']

    metadata_list = []
    
    for record in event['Records']:
        try:
            source_bucket = record['s3']['bucket']['name']
            source_key = record['s3']['object']['key']
            copy_source = {'Bucket': source_bucket, 'Key': source_key}
            event_time = record['eventTime']

            # Prepare metadata string
            metadata_str = f"Filename: {source_key}, Source Bucket: {source_bucket}, Load time: {event_time}\n"
            metadata_list.append(metadata_str)
        except Exception as e:
            logger.error(f'Error extracting file metadata and processing record: {e}')

    for record in event['Records']:
        try:
            source_bucket = record['s3']['bucket']['name']
            source_key = record['s3']['object']['key']
            copy_source = {'Bucket': source_bucket, 'Key': source_key}

            logger.info(f"Copying file {source_key} from bucket {source_bucket} to bucket {trg_bucket}")
            s3.copy_object(
                CopySource=copy_source,
                Bucket=trg_bucket,
                Key=source_key
            )

        except Exception as e:
            logger.error(f"Error copying the file {source_key} from bucket {source_bucket} to bucket {trg_bucket}: {e}")
            raise e

    metadata_content = "".join(metadata_list)

    try:
        s3.put_object(
            Bucket=trg_bucket,
            Key=metadata_filename,
            Body=metadata_content
        )
        logger.info(f'Metadata file created: {metadata_filename}, and loaded into target s3 bucket {trg_bucket}')
    except Exception as e:
        logger.error(f"Error creating metadata file in bucket {trg_bucket}: {e}")
        raise e

    return {
        'statusCode': 200,
        'body': json.dumps('Files copied successfully, metadata file created. Job well done!')
    }
