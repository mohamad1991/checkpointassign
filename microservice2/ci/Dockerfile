FROM python:3.9-slim

# Set working directory in the container
WORKDIR /app

# Copy requirements file and install dependencies
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV AWS_REGION=${AWS_REGION}
ENV SQS_QUEUE_URL=${SQS_QUEUE_URL}
ENV S3_BUCKET_NAME=${S3_BUCKET_NAME}
ENV S3_UPLOAD_PREFIX=${S3_UPLOAD_PREFIX}
ENV POLLING_INTERVAL=${POLLING_INTERVAL}

# Command to run the application
CMD ["python", "app.py"]
