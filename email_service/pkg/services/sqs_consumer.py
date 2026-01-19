import json
import os
import threading
import boto3
from pydantic import ValidationError
from pkg.model.email_request import EmailRequest
from pkg.services.email_services import EmailService

def run_sqs_worker(shutdown_event=None):
    queue_url = os.getenv("SQS_QUEUE_URL", "")
    if queue_url == "":
        return
    # creo client sqs
    sqs = boto3.client("sqs", endpoint_url=os.getenv("AWS_ENDPOINT_URL", "http://localhost:4566"), region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1"), aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID", "test"), aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY", "test"))
    while True:
        if shutdown_event != None and shutdown_event.is_set():
            break
        try:
            resp = sqs.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=1, WaitTimeSeconds=10, VisibilityTimeout=60)
        except Exception as e:
            print("sqs receive fallito:", e)
            continue
        for msg in resp.get("Messages", []):
            if shutdown_event != None and shutdown_event.is_set():
                break
            receipt = msg.get("ReceiptHandle")
            if receipt == None:
                continue
            try:
                body = json.loads(msg["Body"])
            except:
                try:
                    sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt)
                except:
                    pass
                continue
            # il body ha Message che e il nostro payload (sns lo mette cosi)
            raw = body.get("Message")
            if raw == None:
                try:
                    sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt)
                except:
                    pass
                continue
            if isinstance(raw, str):
                try:
                    payload = json.loads(raw)
                except:
                    try:
                        sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt)
                    except:
                        pass
                    continue
            else:
                payload = raw if isinstance(raw, dict) else None
            if payload == None:
                try:
                    sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt)
                except:
                    pass
                continue
            try:
                req = EmailRequest(**payload)
            except ValidationError:
                try:
                    sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt)
                except:
                    pass
                continue
            res = EmailService.send_email(req)
            if res.get("status") == "ok":
                try:
                    sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt)
                except Exception as ex:
                    print("delete_message fallito", ex)
            # se non ok non elimino cosi riprova dopo

def start_sqs_worker_background():
    if os.getenv("SQS_QUEUE_URL", "") == "":
        return None
    ev = threading.Event()
    t = threading.Thread(target=run_sqs_worker, args=(ev,), daemon=True)
    t.start()
    return ev
