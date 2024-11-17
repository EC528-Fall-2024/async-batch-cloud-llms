import requests
import json

# url = "http://127.0.0.1:8080"
url = "https://us-central1-elated-scope-437703-h9.cloudfunctions.net/batch-processor-http"

# external 
#   "User_Project_ID": "sampleproject-440900",
#   "User_Dataset_ID": "user_dataset",
#   "Input_Table_ID": "input_table",
#   "Output_Table_ID": "output2",

# internal 
#   "User_Project_ID": "elated-scope-437703-h9",
#   "User_Dataset_ID": "user_dataset",
#   "Input_Table_ID": "input_table",
#   "Output_Table_ID": "output_table",


payload = json.dumps({
  "Job_ID": "12345",
  "Client_ID": "rick sorkin",
  "User_Project_ID": "sampleproject-440900",
  "User_Dataset_ID": "user_dataset",
  "Input_Table_ID": "input_table",
  "Output_Table_ID": "output2",
  "Model": "model_v1",
  "API_key": "modelKey"
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)