import boto3
import json
import os
from dotenv import load_dotenv

load_dotenv()

sqs = boto3.client(
    "sqs",
    region_name=os.getenv("AWS_REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)

QUEUE_URL = os.getenv("SQS_QUEUE_URL")

def publish_task(task_type: str, target: str):
    """Send a task to the SQS queue."""
    message = json.dumps({"task_type": task_type, "target": target})
    sqs.send_message(QueueUrl=QUEUE_URL, MessageBody=message)
    print(f"Published task: {task_type} for {target}")