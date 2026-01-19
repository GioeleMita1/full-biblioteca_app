import json
import os
import boto3


def publish_email_event(payload):
    topic_arn = os.getenv("SNS_TOPIC_ARN", "")
    if topic_arn == "":
        return
    try:
        sns = boto3.client("sns", endpoint_url=os.getenv("AWS_ENDPOINT_URL", "http://localhost:4566"), region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1"), aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "test"), aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "test"))
        sns.publish(TopicArn=topic_arn, Message=json.dumps(payload))
    except Exception as e:
        # se fallisce non blocco l'app
        print("sns publish fallito:", e)
