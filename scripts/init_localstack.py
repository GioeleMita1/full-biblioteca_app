import json
import os
import time
import boto3

endpoint = os.environ.get("AWS_ENDPOINT_URL", "http://localhost:4566")
region = os.environ.get("AWS_DEFAULT_REGION", "us-east-1")
topic_name = "biblioteca-events"
queue_name = "email-queue"

print("avvio init localstack...")
print("endpoint:", endpoint, "region:", region)

# creo i client boto
sns = boto3.client("sns", endpoint_url=endpoint, region_name=region, aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID", "test"), aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY", "test"))
sqs = boto3.client("sqs", endpoint_url=endpoint, region_name=region, aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID", "test"), aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY", "test"))

# creazione del topic SNS
topic_arn = None
for i in range(12):
    try:
        print("tentativo", i + 1, "- creo topic", topic_name)
        r = sns.create_topic(Name=topic_name)
        topic_arn = r["TopicArn"]
        print("ok topic_arn:", topic_arn)
        break
    except Exception as e:
        err = str(e).lower()
        if "connection" in err or "could not connect" in err or "nodename" in err:
            if i < 11:
                print("localstack non pronto aspetto 5 sec e riprovo")
                time.sleep(5)
            else:
                print("ERRORE: localstack non raggiungibile")
                exit(1)
        else:
            raise

if topic_arn == None:
    print("ERRORE")
    exit(1)

# qua creo la coda SQS
print("creo coda", queue_name)
r = sqs.create_queue(QueueName=queue_name)
queue_url = r["QueueUrl"]
print("queue_url:", queue_url)

# mi serve il QueueArn
res = sqs.get_queue_attributes(QueueUrl=queue_url, AttributeNames=["QueueArn"])
queue_arn = res["Attributes"]["QueueArn"]
print("queue_arn:", queue_arn)

# metto la policy sulla coda cosi SNS puo inviare
policy = {}
policy["Version"] = "2012-10-17"
policy["Statement"] = [{
    "Effect": "Allow",
    "Principal": {"Service": "sns.amazonaws.com"},
    "Action": "sqs:SendMessage",
    "Resource": queue_arn,
    "Condition": {"ArnEquals": {"aws:SourceArn": topic_arn}},
}]
sqs.set_queue_attributes(QueueUrl=queue_url, Attributes={"Policy": json.dumps(policy)})
print("policy impostata")

# subscribe della coda al topic, controllo se ce gia
subs = sns.list_subscriptions_by_topic(TopicArn=topic_arn)
gia_fatto = False
for sub in subs.get("Subscriptions", []):
    if sub.get("Endpoint") == queue_arn and sub.get("SubscriptionArn") != "PendingConfirmation":
        gia_fatto = True
        break
if gia_fatto == False:
    sns.subscribe(TopicArn=topic_arn, Protocol="sqs", Endpoint=queue_arn)
    print("subscription creata")
else:
    print("subscription gia presente skip")

print("fatto!")
print("SNS_TOPIC_ARN=" + topic_arn)
print("SQS_QUEUE_URL=" + queue_url)
