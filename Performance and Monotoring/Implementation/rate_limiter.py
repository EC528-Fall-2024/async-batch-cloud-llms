import requests

# VM URL
base_url = "http://34.27.114.71:8080"

job_id = 1


# Example Calls
#########################
# at the beginning...
decrementQueue1(job_id)
incrementRateLimiter(job_id)

# ...at the end
decrementRateLimiter(job_id)
incrementQueue2(job_id)


######################
# Rate Limiter Calls #
######################
def incrementRateLimiter(Job_ID):
    
    json_body = {"Job_ID": Job_ID,"Microservice": "rate_limiter"}
    headers = {"Content-Type": "application/json"}

    response = requests.get(
        f"{base_url}/incrementService",
        json=json_body,  # Add JSON body
        headers=headers   # Add headers
    )
    
    if response.status_code == 200:
        print("Success") # remove for implemetation
    return "Error"

def decrementRateLimiter(Job_ID):
    
    json_body = {"Job_ID": Job_ID,"Microservice": "rate_limiter"}
    headers = {"Content-Type": "application/json"}

    response = requests.get(
        f"{base_url}/decrementService",
        json=json_body,  # Add JSON body
        headers=headers   # Add headers
    )
    
    if response.status_code == 200:
        print("Success") # remove for implemetation
    return "Error"

# queue calls
def incrementQueue2(Job_ID):
    
    json_body = {"Job_ID": Job_ID,"Microservice": "queue_2"}
    headers = {"Content-Type": "application/json"}

    response = requests.get(
        f"{base_url}/incrementService",
        json=json_body,  # Add JSON body
        headers=headers   # Add headers
    )
    
    if response.status_code == 200:
        print("Success") # remove for implemetation
    return "Error"

def decrementQueue1(Job_ID):
    
    json_body = {"Job_ID": Job_ID,"Microservice": "queue_1"}
    headers = {"Content-Type": "application/json"}

    response = requests.get(
        f"{base_url}/decrementService",
        json=json_body,  # Add JSON body
        headers=headers   # Add headers
    )
    
    if response.status_code == 200:
        print("Success") # remove for implemetation
    return "Error"
