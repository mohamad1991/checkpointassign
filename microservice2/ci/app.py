import os
import time
import json
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

# AWS Configuration
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
SQS_QUEUE_URL = os.getenv("SQS_QUEUE_URL")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
S3_UPLOAD_PREFIX = os.getenv("S3_UPLOAD_PREFIX", "uploads/")
POLLING_INTERVAL = int(os.getenv("POLLING_INTERVAL", 10))  # Default 10 seconds

# AWS Clients
sqs_client = boto3.client("sqs", region_name=AWS_REGION)
s3_client = boto3.client("s3", region_name=AWS_REGION)

def process_message(message_body: str):
    """Process message and upload to S3."""
    try:
        data = json.loads(message_body)
        file_name = f"{S3_UPLOAD_PREFIX}{int(time.time())}.json"
        s3_client.put_object(Bucket=S3_BUCKET_NAME, Key=file_name, Body=json.dumps(data))
        print(f"Uploaded message to s3://{S3_BUCKET_NAME}/{file_name}")
    except json.JSONDecodeError:
        print("Error: Unable to decode message body.")
    except (NoCredentialsError, PartialCredentialsError):
        print("Error: AWS credentials not found or incomplete.")

def poll_sqs():
    """Poll SQS messages and process them."""
    while True:
        try:
            response = sqs_client.receive_message(
                QueueUrl=SQS_QUEUE_URL,
                MaxNumberOfMessages=10,
                WaitTimeSeconds=5
            )
            messages = response.get("Messages", [])

            for message in messages:
                process_message(message["Body"])
                sqs_client.delete_message(QueueUrl=SQS_QUEUE_URL, ReceiptHandle=message["ReceiptHandle"])
                print("Deleted message from SQS")
        except Exception as e:
            print(f"Error: {e}")

        time.sleep(POLLING_INTERVAL)

if __name__ == "__main__":
    print("Starting SQS to S3 microservice...")
    poll_sqs()
