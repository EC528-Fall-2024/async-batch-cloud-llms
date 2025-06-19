import pandas as pd
import csv
import time
from datetime import datetime
from openai import OpenAI
import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# Setup OpenAI API key
os.environ["OPENAI_API_KEY"] = ""
client = OpenAI()

input_csv = "dataset-1000.csv"
output_csv = "responses-multithread-1000.csv"
timing_csv = "response_times-multithread-1000.csv"

# Read the CSV file without a header
df = pd.read_csv(input_csv, header=None)

if df.shape[1] < 2:
    raise ValueError("CSV file must have at least two columns")

second_column_name = df.columns[1]  
requests = df[second_column_name]

responses = []
timings = []

# Format messages for OpenAI
def format_messages(message):
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": message},
    ]
    return messages

# # Function to process each request
# def process_request(request, count):
#     start_time = time.time()
#     message = format_messages(request)

#     try:
#         response = client.chat.completions.create(
#             model="gpt-3.5-turbo",
#             messages=message
#         )
#         response_text = response.choices[0].message.content.strip()
#         actual = response.usage.total_tokens
#     except Exception as e:
#         response_text = f"Error: {str(e)}"

#     # Collect data for response and timing
#     responses.append({"response": response_text})
#     timings.append({
#         "Elapsed Time (s)": time.time() - start_time,
#         "Row Count": count
#     })

import time
import re

def process_request(request, count, max_retries=15):
    start_time = time.time()
    message = format_messages(request)
    
    retries = 0
    while retries < max_retries:
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=message
            )
            response_text = response.choices[0].message.content.strip()
            actual = response.usage.total_tokens
            break  # If successful, exit loop
        except Exception as e:
            if 'Rate limit' in str(e):
                # Extract suggested wait time from error message using regex
                match = re.search(r"Please try again in (\d+)ms", str(e))
                if match:
                    wait_time_ms = int(match.group(1)) / 1000  # Convert to seconds
                    print(f"Rate limit reached. Waiting for {wait_time_ms:.2f} seconds...")
                    time.sleep(wait_time_ms)  # Wait for the suggested time
                    retries += 1
                    if retries >= max_retries:
                        response_text = f"Error: Rate limit exceeded after {retries} retries."
                        break
                else:
                    response_text = f"Error: Unable to extract wait time from rate limit message."
                    break
            else:
                response_text = f"Error: {str(e)}"
                break

    # Collect data for response and timing
    responses.append({"response": response_text})
    timings.append({
        "Elapsed Time (s)": start_time,
        "Row Count": count,
        "Retries": retries
    })

# Use ThreadPoolExecutor to process requests concurrently
with ThreadPoolExecutor(max_workers=10) as executor:
    future_to_request = {executor.submit(process_request, request, count): request for count, request in enumerate(requests, 1)}

    # Wait for all futures to complete
    for future in as_completed(future_to_request):
        pass

# Convert to DataFrames
response_df = pd.DataFrame(responses)
timing_df = pd.DataFrame(timings)

# Append responses to CSV
response_df.to_csv(output_csv, mode='a', index=False, quoting=csv.QUOTE_ALL)
timing_df.to_csv(timing_csv, mode='a', index=False, quoting=csv.QUOTE_ALL)

print(f"Responses saved to {output_csv}")
print(f"Response times saved to {timing_csv}")