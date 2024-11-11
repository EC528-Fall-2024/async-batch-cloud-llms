'''Temporary Log Listener'''
from google.cloud import pubsub_v1
import threading

# Prepare all three topics
project_id = "elated-scope-437703-h9"
logging_id = "GeneralLogs-sub"
progress_id = "ProgressLogs-sub"
error_id = "ErrorLogs-sub"

# Callback for each type of log
def log(message):
    print(f"Received log message: {message}")
    message.ack()

def progress(message):
    print(f"Received progress message: {message}")
    message.ack()

def error(message):
    print(f"Received error message: {message}")
    message.ack()

# Functions to subscribe
def log_subscribe():
    subscriber = pubsub_v1.SubscriberClient()
    log_path = subscriber.subscription_path(project_id, logging_id)
    streaming_pull_future = subscriber.subscribe(f"{log_path}", callback=log)
    print(f"Listening for messages on {log_path}..\n")
    with subscriber:
        try:
            streaming_pull_future.result()
        except:
            streaming_pull_future.cancel() 

def progress_subscribe():
    subscriber = pubsub_v1.SubscriberClient()
    progress_path = subscriber.subscription_path(project_id, progress_id)
    streaming_pull_future = subscriber.subscribe(f"{progress_path}", callback=progress)
    print(f"Listening for messages on {progress_path}..\n")
    with subscriber:
        try:
            streaming_pull_future.result()
        except:
            streaming_pull_future.cancel() 

def error_subscribe():
    subscriber = pubsub_v1.SubscriberClient()
    error_path = subscriber.subscription_path(project_id, error_id)
    streaming_pull_future = subscriber.subscribe(f"{error_path}", callback=error)
    print(f"Listening for messages on {error_path}..\n")
    with subscriber:
        try:
            streaming_pull_future.result()
        except:
            streaming_pull_future.cancel() 

if __name__ == "__main__":
    # start continuous subscribers as three separate threads 
    threading.Thread(target=log_subscribe).start()
    threading.Thread(target=progress_subscribe).start()
    threading.Thread(target=error_subscribe).start()

    # need to break manually
    while True:
        continue