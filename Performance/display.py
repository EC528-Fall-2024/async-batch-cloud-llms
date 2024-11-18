import requests
import time

# Define the URL for the endpoints
# base_url = "http://localhost:8084"

# Container URL
# base_url = "https://performance-api-1069651367433.us-central1.run.app"

# VM URL
base_url = "http://34.27.114.71:8080"

# Function to get batch processor count
def get_batch_processor_load():

    json_body = {"Job_ID": 1,"Microservice": "batch_processor"}
    headers = {"Content-Type": "application/json"}

    response = requests.get(
        f"{base_url}/getCount",
        json=json_body,  # Add JSON body
        headers=headers   # Add headers
    )

    if response.status_code == 200:
        # print(response.json())
        # print(getattr(response.json(), ("batch_processor")))
        return response.json().get("batch_processor_count")
    return "Error"

def get_total_rows():
    
    json_body = {"Job_ID": 1,"Microservice": "total"}
    headers = {"Content-Type": "application/json"}

    response = requests.get(
        f"{base_url}/getCount",
        json=json_body,  # Add JSON body
        headers=headers   # Add headers
    )
    
    if response.status_code == 200:
        return response.json().get("total_count", "N/A")
    return "Error"

# Function to get rate limiter count
def get_rate_limiter_load():
    
    json_body = {"Job_ID": 1,"Microservice": "rate_limiter"}
    headers = {"Content-Type": "application/json"}

    response = requests.get(
        f"{base_url}/getCount",
        json=json_body,  # Add JSON body
        headers=headers   # Add headers
    )
    
    if response.status_code == 200:
        return response.json().get("rate_limiter_count", "N/A")
    return "Error"

# Function to get reverse batch processor count
def get_reverse_batch_processor_load():
    
    json_body = {"Job_ID": 1,"Microservice": "reverse_batch_processor"}
    headers = {"Content-Type": "application/json"}

    response = requests.get(
        f"{base_url}/getCount",
        json=json_body,  # Add JSON body
        headers=headers   # Add headers
    )
    
    if response.status_code == 200:
        return response.json().get("reverse_batch_processor_count", "N/A")
    return "Error"



# Loop to update and display counts every half-second
try:
    while True:
        # Get the latest values from each endpoint
        batch_processor_count = get_batch_processor_load()
        rate_limiter_count = get_rate_limiter_load()
        reverse_batch_processor_count = get_reverse_batch_processor_load()
        total_rows = get_total_rows()

        
        # Clear the console (works in most terminal environments)
        print("\033c", end="")  # This clears the screen in most terminal environments
        
        # Display the updated values
        print("### Live Processor Counts ###")
        print(f"Batch Processor Count: {batch_processor_count} / {total_rows}")
        print(f"Rate Limiter Count: {rate_limiter_count} / {total_rows}")
        print(f"Reverse Batch Processor Count: {reverse_batch_processor_count} / {total_rows}")
        
        # Wait for half a second before updating
        time.sleep(0.2)

except KeyboardInterrupt:
    print("Stopped updating.")