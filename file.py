import boto3
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    bucket_name = 'production01-bucket'
    
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)

    try:
        bucket.objects.all().delete()
        logger.info(f"All objects in bucket {bucket_name} have been deleted.")
    except Exception as e:
        logger.error(f"Error deleting objects from bucket {bucket_name}: {str(e)}")
        raise e
