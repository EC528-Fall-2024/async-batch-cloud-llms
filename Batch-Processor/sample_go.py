import requests

url = "http://localhost:5004/go"
data = {
    "Job_ID": "job43",
    "Client_ID": "rick sorkin",
    "Database_Length": "13"
}

response = requests.post(url, json=data)
print(response.json())
