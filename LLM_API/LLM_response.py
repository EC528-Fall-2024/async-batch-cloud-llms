from datasets import load_dataset
from tqdm import tqdm
import os
import time
from queue import Queue
import threading
from openai import OpenAI
from dotenv import load_dotenv
import signal

load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set. Please set it before running this script.")

client = OpenAI(api_key=openai_api_key)

class SampleStorageBucket:
    def __init__(self):
        self.bucket= []
    
    def write(self, data):
        self.bucket .append(data)
    

class SampleLimiter:
    def __init__(self, rate_limit):
        self.rate_limit = rate_limit
        self.tokens = rate_limit
        self.last_refill = time.time()
    
    def wait(self, tokens):
        while self.tokens < tokens:
            now = time.time()
            time_passed = now - self.last_refill
            self.tokens = min(self.rate_limit, self.tokens + time_passed * (self.rate_limit / 60))
            if self.tokens < tokens:
                time.sleep(.1)
            self.tokens -= tokens

# Response Queue for deciphering inf
llm_response_queue = Queue()

# User's Output Bucket 
output_bucket = SampleStorageBucket()

data = load_dataset("stanford-oval/ccnews", name="2016", streaming=True) # `name` can be one of 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024

shutdown_flag = threading.Event()

# Sample Limiting Function
def process(batch):
    rate_limiter = SampleLimiter(60)  # 60 requests per minute
    for item in batch:
        if shutdown_flag.is_set():
            break
        rate_limiter.wait(1)  # Wait for 1 token (1 request)
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that summarizes news articles."},
                    {"role": "user", "content": f"Summarize this news article in one sentence: {item['title']}"}
                ]
            )
            summary = response.choices[0].message.content.strip()
            llm_response_queue.put({"title": item["title"], "summary": summary})
        except Exception as e:
            print(f"Error processing item: {str(e)}")
            if "insufficient_quota" in str(e):
                print("You have exceeded your OpenAI API quota. Please check your plan and billing details.")
                shutdown_flag.set()
                break


def rev_process():
    while not shutdown_flag.is_set():
        try:
            resp = llm_response_queue.get()
            if resp is None:
                break
            output_bucket.write(resp)
            llm_response_queue.task_done()
        except Queue.empty:
            continue
    
def signal_handler(signum, frame):
    print('\nInterrupt received, shutting down')
    shutdown_flag.set()

signal.signal(signal.SIGINT, signal_handler)

# Start rev batch processor thread
print('\nCreated reverse process')
rev_process_thread = threading.Thread(target=rev_process)
print('\nStarting reverse process')
rev_process_thread.start()

# Not sure if this helps or not 
batch_size = 2
batch = []

print('\nAppending batches')
for i, example in  enumerate(tqdm(data['train'])):
    batch.append(example)
    if len(batch) == batch_size:
        process(batch)
        batch = []

# Process remaining
print('\nProcessing remaining batches')
if batch:
    process(batch)

# Signal Rev Batch Processor to finish
print('Signalling Rev Batch to finish')
llm_response_queue.put(None)

# Wait for tasks to be processed
print('Waiting Rev Batch to finish')
llm_response_queue.join()

# Wait for rev processor to finish
rev_process_thread.join()

# Print results
print("\nProcessed summaries:")
for item in output_bucket.data[:5]: # Print only first 5 summaries, I think
    print(f"Title: {item['title'][:50]}..., Summary: {item['summary']}")

print(f'\nTotal processed items: {len(output_bucket.bucket)}')
