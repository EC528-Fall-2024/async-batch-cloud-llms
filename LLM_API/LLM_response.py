from datasets import load_dataset
from tqdm import tqdm
import os
import time
from queue import Queue, Empty
import threading
from dotenv import load_dotenv
import signal
from openai import OpenAI
import atexit

load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set. Please set it before running this script.")

client = OpenAI(api_key=openai_api_key)

class SampleStorageBucket:
    def __init__(self):
        self.bucket = []
    
    def write(self, data):
        self.bucket.append(data)
    
    @property
    def data(self):
        return self.bucket

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
            self.last_refill = now
            if self.tokens < tokens:
                time.sleep(.1)
        self.tokens -= tokens

llm_response_queue = Queue()
output_bucket = SampleStorageBucket()
shutdown_flag = threading.Event()
processing_complete = threading.Event()
interrupt_count = 0

def process(batch):
    rate_limiter = SampleLimiter(60)
    for item in batch:
        if shutdown_flag.is_set():
            print("Shutdown flag set, exiting process")
            return
        
        rate_limiter.wait(1)
        try:
            print(f"Processing review: {item['sentence'][:50]}...")

            #  Define what type of OpenAI generation want to use
            # TODO: Make this a variable later to allow user input
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that analyzes movie reviews."},
                    {"role": "user", "content": f"Analyze the sentiment of this movie review in one word (happy or sad): {item['sentence']}"}
                ]
            )
            analysis = response.choices[0].message.content.strip()
            llm_response_queue.put({"sentence": item["sentence"], "analysis": analysis})
            print(f"Analysis complete: {analysis}")
        except Exception as e:
            print(f"Error processing item: {str(e)}")
            # Ran out of credits
            if "insufficient_quota" in str(e):
                print("You have exceeded your OpenAI API quota. Please check your plan and billing details.")
                shutdown_flag.set()
                return
            else:
                print(f"Unknown error: {e}")

def rev_process():
    while not (processing_complete.is_set() and llm_response_queue.empty()):
        try:
            resp = llm_response_queue.get(timeout=1)
            if resp is None:
                break
            output_bucket.write(resp)
            llm_response_queue.task_done()
            print(f"Stored analysis for: {resp['sentence'][:50]}... -> {resp['analysis']}")
        except Empty:
            if shutdown_flag.is_set():
                break
            continue
        except Exception as e:
            print(f"Error in rev_process: {str(e)}")
    print("Reverse process completed")

def signal_handler(signum, frame):
    global interrupt_count
    interrupt_count += 1
    if interrupt_count == 1:
        print('\nInterrupt received, shutting down...')
        shutdown_flag.set()
        processing_complete.set()
    elif interrupt_count >= 2:
        print('\nForce quitting...')
        os._exit(0)

def cleanup():
    if not shutdown_flag.is_set():
        shutdown_flag.set()
    if not processing_complete.is_set():
        processing_complete.set()

def main():
    atexit.register(cleanup)
    signal.signal(signal.SIGINT, signal_handler)

    print("Starting sentiment analysis processing...")
    rev_process_thread = threading.Thread(target=rev_process)
    rev_process_thread.daemon = True
    rev_process_thread.start()

    # Load and process data
    data = load_dataset('glue', 'sst2')['train'].select(range(5))
    batch_size = 2
    batch = []

    try:
        for i, example in enumerate(tqdm(data, desc="Processing reviews")):
            if shutdown_flag.is_set():
                break
            batch.append(example)
            if len(batch) == batch_size:
                process(batch)
                batch = []

        if batch and not shutdown_flag.is_set():
            process(batch)

    finally:
        processing_complete.set()
        print("\nAll reviews processed, finalizing results...")
        
        # Ensure queue is properly closed
        if not llm_response_queue.empty():
            llm_response_queue.put(None)
        
        # Wait for processing to complete
        try:
            llm_response_queue.join()
            rev_process_thread.join(timeout=3)
        except:
            pass

        # Print results
        if output_bucket.data:
            print("\nFinal Results:")
            print("-" * 50)
            for i, item in enumerate(output_bucket.data, 1):
                print(f"\n{i}. Review: {item['sentence'][:100]}...")
                print(f"   Analysis: {item['analysis']}")
            print(f"\nTotal processed items: {len(output_bucket.data)}")
        else:
            print("\nNo results were processed.")

if __name__ == "__main__":
    main()