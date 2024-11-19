import requests

# VM URL
base_url = "http://34.27.114.71:8080"

job_id = 1

# Example Calls
#########################
decrementBatchProcessor(job_id)
incrementQueue1(job_id)
        


#########################
# Batch Processor Calls #
#########################

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
        print("Success") # remove for implemetation
    return "Error"