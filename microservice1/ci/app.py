from flask import Flask, request, jsonify
import requests
import boto3
import os
import json
import logging
from datetime import datetime
from botocore.exceptions import ClientError

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# AWS clients
ssm_client = boto3.client("ssm")
sqs_client = boto3.client("sqs")

# Retrieve token from AWS Secrets Manager
SECRETS_MANAGER_NAME = "your-secrets-manager-name"

def get_secret():
    try:
        secrets_client = boto3.client("secretsmanager")
        response = secrets_client.get_secret_value(SecretId=SECRETS_MANAGER_NAME)
        return json.loads(response["SecretString"]).get("token")
    except ClientError as e:
        logger.error(f"Error retrieving secret: {e}")
        return None

TOKEN = get_secret()

# SQS Queue URL
SQS_QUEUE_URL = "your-sqs-queue-url"

def validate_request(data):
    if not data or "token" not in data or "data" not in data or "email_content" not in data:
        return False, "Invalid JSON payload"

    if data["token"] != TOKEN:
        return False, "Invalid token"

    if "email_timestream" not in data["data"]:
        return False, "Missing email_timestream field"

    try:
        datetime.utcfromtimestamp(int(data["data"]["email_timestream"]))
    except ValueError:
        return False, "Invalid email_timestream format"

    return True, ""

@app.route("/forward", methods=["POST"])
def forward_request():
    try:
        data = request.get_json()
        is_valid, error_message = validate_request(data)
        if not is_valid:
            return jsonify({"error": error_message}), 400

        # Publish message to SQS
        sqs_client.send_message(
            QueueUrl=SQS_QUEUE_URL,
            MessageBody=json.dumps(data)
        )

        logger.info("Message successfully published to SQS")
        return jsonify({"message": "Request successfully published to SQS"}), 200

    except ClientError as e:
        logger.error(f"AWS ClientError: {e}")
        return jsonify({"error": "AWS service error"}), 500
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
