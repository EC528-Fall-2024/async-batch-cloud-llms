import requests

# Performance VM URL
base_url = "http://34.27.114.71:8080"

# Rate Limiter Calls 
def incrementRateLimiter(Job_ID):
    json_body = {"Job_ID": Job_ID,"Microservice": "rate_limiter"}
    headers = {"Content-Type": "application/json"}
    requests.get(
        f"{base_url}/incrementService",
        json=json_body,  # Add JSON body
        headers=headers   # Add headers
    )

def decrementRateLimiter(Job_ID):
    json_body = {"Job_ID": Job_ID,"Microservice": "rate_limiter"}
    headers = {"Content-Type": "application/json"}
    requests.get(
        f"{base_url}/decrementService",
        json=json_body,  # Add JSON body
        headers=headers   # Add headers
    )

# Queue calls
def incrementQueue2(Job_ID):
    json_body = {"Job_ID": Job_ID,"Microservice": "queue_2"}
    headers = {"Content-Type": "application/json"}
    requests.get(
        f"{base_url}/incrementService",
        json=json_body,  # Add JSON body
        headers=headers   # Add headers
    )

def decrementQueue1(Job_ID):
    json_body = {"Job_ID": Job_ID,"Microservice": "queue_1"}
    headers = {"Content-Type": "application/json"}
    requests.get(
        f"{base_url}/decrementService",
        json=json_body,  # Add JSON body
        headers=headers   # Add headers
    )
