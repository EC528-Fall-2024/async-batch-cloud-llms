import requests
import json

######
######
# This is a mock batch processor caller.
# Run this script, and the batch processor will be invoked

# Developed by Noah Robitshek Nov 18th, 2024
#####
#####

#CHANGE IF WRONT LOL
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
def call_batch_processor():
  payload = json.dumps({
    "Job_ID": "1",
    "Client_ID": "rick sorkin",
    "User_Project_ID": "sampleproject-440900",
    "User_Dataset_ID": "user_dataset",
    "Input_Table_ID": "input_table",
    "Output_Table_ID": "output_2",
    "Model": "gpt-3.5-turbo",
    "API_key": "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"
  })
  headers = {
    'Content-Type': 'application/json'
  }

  response = requests.request("POST", url, headers=headers, data=payload)

  print(response.text)
  
call_batch_processor()
