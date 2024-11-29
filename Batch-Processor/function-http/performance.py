import requests

# VM URL
base_url = "http://34.27.114.71:8080"

def decrementBatchProcessor(Job_ID):
    
    json_body = {"Job_ID": Job_ID,"Microservice": "batch_processor"}
    headers = {"Content-Type": "application/json"}

    response = requests.get(
        f"{base_url}/decrementService",
        json=json_body,  # Add JSON body
        headers=headers   # Add headers
    )
    
    if response.status_code == 200:
        return
    return "Error"

# queue calls
def incrementQueue1(Job_ID):
    
    json_body = {"Job_ID": Job_ID,"Microservice": "queue_1"}
    headers = {"Content-Type": "application/json"}

    response = requests.get(
        f"{base_url}/incrementService",
        json=json_body,  # Add JSON body
        headers=headers   # Add headers
    )
    
    if response.status_code == 200:
        return
    return "Error"


def setTotalCount(Job_ID):
    
    json_body = {"Job_ID": Job_ID, "total_count": 13}
    headers = {"Content-Type": "application/json"}

    response = requests.get(
        f"{base_url}/setTotalCount",
        json=json_body,  # Add JSON body
        headers=headers   # Add headers
    )
    
    if response.status_code == 200:
        return
    return "Error"

def setBatchProcessor(Job_ID):
    
    json_body = {"Job_ID": 1, "batch_processor_count": 13}
    headers = {"Content-Type": "application/json"}

    response = requests.get(
        f"{base_url}/setBatchProcessorCount",
        json=json_body,  # Add JSON body
        headers=headers   # Add headers
    )
    
    if response.status_code == 200:
        return
    return "Error"

def resetSystem(Job_ID):
    
    json_body = {"Job_ID": Job_ID}
    headers = {"Content-Type": "application/json"}

    response = requests.get(
        f"{base_url}/resetSystem",
        json=json_body,  # Add JSON body
        headers=headers   # Add headers
    )
    
    if response.status_code == 200:
        return
    return "Error"

