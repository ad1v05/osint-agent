import json 
import os 
from dotenv import load_dotenv
import boto3
from agent.tasks import lookup_ip, lookup_news, lookup_shodan, lookup_whois

load_dotenv()

sqs = boto3.client(
    "sqs",
    region_name=os.getenv("AWS_REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)
# this sets up the SQS client using the AWS credentials and region from the .env file

QUEUE_URL = os.getenv("SQS_QUEUE_URL")

TASK_MAP = {
    "ip": lookup_ip,
    "news": lookup_news,
    "shodan": lookup_shodan,
    "whois": lookup_whois
}
# this maps the task types to their corresponding functions 

def consume():
    """Poll the queue and execute tasks as they arrive."""
    print("Polling SQS Queue...")
    while True:
        response = sqs.receive_message(
            QueueUrl=QUEUE_URL,
            MaxNumberOfMessages=5,
            WaitTimeSeconds=10
        )
        # this polls the SQS queue for messages, it waits for up to 10 seconds and retrieves up to 5 messages at a time
        messages = response.get("Messages", [])
        if not messages: 
            print("Queue empty. Done")
            break
        # this checks if there are any messages in the queue, if not it prints a message
        for msg in messages:
            body = json.loads(msg["Body"])
            task_type = body.get("task_type")
            target = body.get("target")
            print(f"Processign task: {task_type} for {target}")
            task_fn = TASK_MAP.get(task_type)
            # this retrieves the corresponding function for the task type from the TASK_MAP
            if task_fn:
                result = task_fn(target)
                print(f"Result: {json.dumps(result, indent=2)}")
                # this executes the task function with the target and prints the result in a formatted way
            sqs.delete_message(
                QueueUrl=QUEUE_URL,
                ReceiptHandle=msg["ReceiptHandle"]
            )
            print(f"Task complete: {task_type}")
            
if __name__ == "__main__":
    consume()