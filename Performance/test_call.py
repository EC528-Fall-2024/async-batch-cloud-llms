import requests
import time


base_url = "http://127.0.0.1:8084"
# base_url = "something deployed"




###################
# Set/Reset Calls #
###################
def resetSystem():
    
    json_body = {"Job_ID": 1}
    headers = {"Content-Type": "application/json"}

    response = requests.get(
        f"{base_url}/resetSystem",
        json=json_body,  # Add JSON body
        headers=headers   # Add headers
    )
    
    if response.status_code == 200:
        print("Success") # remove for implemetation
    return "Error"

def setTotalCount():
    
    json_body = {"Job_ID": 1, "total_count": 10}
    headers = {"Content-Type": "application/json"}

    response = requests.get(
        f"{base_url}/setTotalCount",
        json=json_body,  # Add JSON body
        headers=headers   # Add headers
    )
    
    if response.status_code == 200:
        print("Success") # remove for implemetation
    return "Error"

def setBatchProcessor():
    
    json_body = {"Job_ID": 1, "batch_processor_count": 10}
    headers = {"Content-Type": "application/json"}

    response = requests.get(
        f"{base_url}/setBatchProcessorCount",
        json=json_body,  # Add JSON body
        headers=headers   # Add headers
    )
    
    if response.status_code == 200:
        print("Success") # remove for implemetation
    return "Error"



#########################
# Batch Processor Calls #
#########################
def incrementBatchProcessor():
    
    json_body = {"Job_ID": 1,"Microservice": "batch_processor"}
    headers = {"Content-Type": "application/json"}

    response = requests.get(
        f"{base_url}/incrementService",
        json=json_body,  # Add JSON body
        headers=headers   # Add headers
    )
    
    if response.status_code == 200:
        print("Success") # remove for implemetation
    return "Error"

def decrementBatchProcessor():
    
    json_body = {"Job_ID": 1,"Microservice": "batch_processor"}
    headers = {"Content-Type": "application/json"}

    response = requests.get(
        f"{base_url}/decrementService",
        json=json_body,  # Add JSON body
        headers=headers   # Add headers
    )
    
    if response.status_code == 200:
        print("Success") # remove for implemetation
    return "Error"

######################
# Rate Limiter Calls #
######################
def incrementRateLimiter():
    
    json_body = {"Job_ID": 1,"Microservice": "rate_limiter"}
    headers = {"Content-Type": "application/json"}

    response = requests.get(
        f"{base_url}/incrementService",
        json=json_body,  # Add JSON body
        headers=headers   # Add headers
    )
    
    if response.status_code == 200:
        print("Success") # remove for implemetation
    return "Error"

def decrementRateLimiter():
    
    json_body = {"Job_ID": 1,"Microservice": "rate_limiter"}
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
def incrementReverseBatchProcessor():
    
    json_body = {"Job_ID": 1,"Microservice": "reverse_batch_processor"}
    headers = {"Content-Type": "application/json"}

    response = requests.get(
        f"{base_url}/incrementService",
        json=json_body,  # Add JSON body
        headers=headers   # Add headers
    )
    
    if response.status_code == 200:
        print("Success") # remove for implemetation
    return "Error"


def decrementReverseBatchProcessor():
    
    json_body = {"Job_ID": 1,"Microservice": "reverse_batch_processor"}
    headers = {"Content-Type": "application/json"}

    response = requests.get(
        f"{base_url}/decrementService",
        json=json_body,  # Add JSON body
        headers=headers   # Add headers
    )
    
    if response.status_code == 200:
        print("Success") # remove for implemetation
    return "Error"
    
    
if (__name__ == "__main__"):
    
    time.sleep(2)
    
    resetSystem()
    time.sleep(2)

    #init the system
    setTotalCount()
    setBatchProcessor()
    time.sleep(2)


    # decrement batch processor, increment rate limiter
    for i in range(10):
        decrementBatchProcessor()
        incrementRateLimiter()
        time.sleep(1)
        
    # decrement rate limiter, decrement rate limiter
    for i in range(10):
        decrementRateLimiter()
        incrementReverseBatchProcessor()
        time.sleep(1)

