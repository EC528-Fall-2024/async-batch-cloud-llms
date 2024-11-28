import requests
import time

# Local URL
# base_url = "http://127.0.0.1:8084"

# VM URL
base_url = "http://34.27.114.71:8080"

# Container URL
# base_url = "something deployed"


###################
# Set/Reset Calls #
###################
def resetSystem(Job_ID):
    
    json_body = {"Job_ID": Job_ID}
    headers = {"Content-Type": "application/json"}

    response = requests.get(
        f"{base_url}/resetSystem",
        json=json_body,  # Add JSON body
        headers=headers   # Add headers
    )
    
    if response.status_code == 200:
        print("Success") # remove for implemetation
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
        print("Success") # remove for implemetation

def setBatchProcessor(Job_ID):
    
    json_body = {"Job_ID": 1, "batch_processor_count": 13}
    headers = {"Content-Type": "application/json"}

    response = requests.get(
        f"{base_url}/setBatchProcessorCount",
        json=json_body,  # Add JSON body
        headers=headers   # Add headers
    )
    
    if response.status_code == 200:
        print("Success") # remove for implemetation



#########################
# Batch Processor Calls #
#########################
def incrementBatchProcessor(Job_ID):
    
    json_body = {"Job_ID": Job_ID,"Microservice": "batch_processor"}
    headers = {"Content-Type": "application/json"}

    response = requests.get(
        f"{base_url}/incrementService",
        json=json_body,  # Add JSON body
        headers=headers   # Add headers
    )
    
    if response.status_code == 200:
        print("Success") # remove for implemetation
    return "Error"

def decrementBatchProcessor(Job_ID):
    
    json_body = {"Job_ID": Job_ID,"Microservice": "batch_processor"}
    headers = {"Content-Type": "application/json"}

    response = requests.get(
        f"{base_url}/decrementService",
        json=json_body,  # Add JSON body
        headers=headers   # Add headers
    )
    
    if response.status_code == 200:
        print("Success") # remove for implemetation

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
        print("Success") # remove for implemetation
    return "Error"

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

################################
# Reverse Batch Processor Call #
################################
def incrementReverseBatchProcessor(Job_ID):
    
    json_body = {"Job_ID": Job_ID,"Microservice": "reverse_batch_processor"}
    headers = {"Content-Type": "application/json"}

    response = requests.get(
        f"{base_url}/incrementService",
        json=json_body,  # Add JSON body
        headers=headers   # Add headers
    )
    
    if response.status_code == 200:
        print("Success") # remove for implemetation
    return "Error"


def decrementReverseBatchProcessor(Job_ID):
    
    json_body = {"Job_ID": Job_ID,"Microservice": "reverse_batch_processor"}
    headers = {"Content-Type": "application/json"}

    response = requests.get(
        f"{base_url}/decrementService",
        json=json_body,  # Add JSON body
        headers=headers   # Add headers
    )
    
    if response.status_code == 200:
        print("Success") # remove for implemetation
    return "Error"


def decrementQueue2(Job_ID):
    
    json_body = {"Job_ID": Job_ID,"Microservice": "queue_2"}
    headers = {"Content-Type": "application/json"}

    response = requests.get(
        f"{base_url}/decrementService",
        json=json_body,  # Add JSON body
        headers=headers   # Add headers
    )
    
    if response.status_code == 200:
        print("Success") # remove for implemetation
    return "Error"
    
    
    
# INSTRUCTIONS
# Below is a Mock of of the microservices
# As you can see the microervices will first reset the system 
# Then they will start incrementing and decremeting.
if (__name__ == "__main__"):
    job_id = 1
    
    timeDelay = .3
    
    time.sleep(2)
    
    resetSystem(job_id)
    time.sleep(2)

    #init the system
    setTotalCount(job_id)
    setBatchProcessor(job_id)
    time.sleep(2)

    # Batch Processor
    # decrement batch processor, increment queue_1
    for i in range(13):
        decrementBatchProcessor(job_id)
        incrementQueue1(job_id)
        
        time.sleep(timeDelay)
    
    # Rate Limiter
    # decrement queue_1, increment rate limiter
    for i in range(13):
        decrementQueue1(job_id)
        incrementRateLimiter(job_id)
        
        time.sleep(timeDelay)
    
    # Rate Limiter   
    # decrement rate limiter, increment queue_2
    for i in range(13):
        decrementRateLimiter(job_id)
        incrementQueue2(job_id)
        
        time.sleep(timeDelay)
        
    # Reverse Batch Processor
    # decrement queue_2, increment reverse batch processor
    for i in range(13):
        decrementQueue2(job_id)
        incrementReverseBatchProcessor(job_id)
        
        time.sleep(timeDelay)
        
        

