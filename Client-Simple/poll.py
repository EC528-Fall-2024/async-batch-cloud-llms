import requests
import json

def poll_job_status():
    # Ask for the job_id
    job_id = input("Please enter the job_id: ")

    # Define the endpoint URL
    base_url = "https://user-api-1069651367433.us-east4.run.app"
    endpoint = f"{base_url}/job_status/{job_id}"

    try:
        # Make a GET request to the endpoint
        response = requests.get(endpoint)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            job_data = response.json()
            print("Job status:")
            print(json.dumps(job_data, indent=2))
        elif response.status_code == 404:
            print("Error: Job not found")
        else:
            print(f"Error: Unexpected status code {response.status_code}")
            print(response.text)

    except requests.RequestException as e:
        print(f"Error making request: {e}")

if __name__ == "__main__":
    poll_job_status()