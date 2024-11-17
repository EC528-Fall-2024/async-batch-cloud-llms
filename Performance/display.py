import requests
import time

# Define the URL for the endpoints
base_url = "http://localhost:8084"

# Function to get batch processor count
def get_batch_processor_load():
    response = requests.get(f"{base_url}/getBatchProcessorLoad")
    if response.status_code == 200:
        return response.json().get("batch_processor_count", "N/A")
    return "Error"

def get_total_rows():
    response = requests.get(f"{base_url}/getTotalRows")
    if response.status_code == 200:
        return response.json().get("total_count", "N/A")
    return "Error"

# Function to get rate limiter count
def get_rate_limiter_load():
    response = requests.get(f"{base_url}/getRateLimiterLoad")
    if response.status_code == 200:
        return response.json().get("rate_limiter_count", "N/A")
    return "Error"

# Function to get reverse batch processor count
def get_reverse_batch_processor_load():
    response = requests.get(f"{base_url}/getReverseBatchProcessorLoad")
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