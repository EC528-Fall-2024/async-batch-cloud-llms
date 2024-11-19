import requests

# Performance VM URL
base_url = "http://34.27.114.71:8080"

# Reverse Batch Processor 
def incrementReverseBatchProcessor(Job_ID): 
    json_body = {"Job_ID": Job_ID,"Microservice": "reverse_batch_processor"}
    headers = {"Content-Type": "application/json"}
    requests.get(
        f"{base_url}/incrementService",
        json=json_body,  # Add JSON body
        headers=headers   # Add headers
    )

# Queue
def decrementQueue2(Job_ID):   
    json_body = {"Job_ID": Job_ID,"Microservice": "queue_2"}
    headers = {"Content-Type": "application/json"}
    requests.get(
        f"{base_url}/decrementService",
        json=json_body,  # Add JSON body
        headers=headers   # Add headers
    )