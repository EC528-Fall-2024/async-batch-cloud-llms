from datasets import load_dataset
from tqdm import tqdm
import os
import time
from queue import Queue, Empty
import threading
from dotenv import load_dotenv
import signal
import sys
from openai import OpenAI
from dataclasses import dataclass
from typing import List, Dict, Any

load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set.")

client = OpenAI(api_key=openai_api_key)

@dataclass
class Batch:
    items: List[Dict[str, Any]]
    batch_id: int

class RateLimiter:
    def __init__(self, rate_limit: int, llm_queue: Queue):
        self.rate_limit = rate_limit
        self.tokens = rate_limit
        self.last_refill = time.time()
        self.llm_queue = llm_queue
        self.lock = threading.Lock()
    
    def wait(self, tokens: int):
        with self.lock:
            while self.tokens < tokens:
                now = time.time()
                time_passed = now - self.last_refill
                self.tokens = min(self.rate_limit, 
                                self.tokens + time_passed * (self.rate_limit / 60))
                self.last_refill = now
                if self.tokens < tokens:
                    time.sleep(.1)
            self.tokens -= tokens

    def process_batch(self, batch: Batch) -> bool:
        responses = []
        print(f"\nProcessing batch {batch.batch_id} with {len(batch.items)} items...")
        
        for item in batch.items:
            if shutdown_flag.is_set():
                return False
            
            self.wait(1)
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant that analyzes movie reviews."},
                        {"role": "user", "content": f"Analyze the sentiment of this movie review in one word (positive or negative): {item['sentence']}"}
                    ]
                )
                analysis = response.choices[0].message.content.strip().lower()
                responses.append({
                    "sentence": item['sentence'],
                    "analysis": analysis,
                    "batch_id": batch.batch_id
                })
                print(f"✓ Review analyzed: '{item['sentence'][:50]}...' → {analysis}")
                
            except Exception as e:
                print(f"✗ Error in batch {batch.batch_id}: {str(e)}")
                if "insufficient_quota" in str(e):
                    shutdown_flag.set()
                    return False
        
        if responses:
            self.llm_queue.put(responses)
            print(f"→ Batch {batch.batch_id} sent to processing queue")
            return True
        return False

class ReverseBatchProcessor(threading.Thread):
    def __init__(self, llm_queue: Queue, output_bucket: 'OutputBucket'):
        super().__init__()
        self.llm_queue = llm_queue
        self.output_bucket = output_bucket
        self.daemon = True
        
    def run(self):
        print("\nReverse batch processor started...")
        while True:
            try:
                batch_responses = self.llm_queue.get(timeout=1)
                if batch_responses is None:
                    print("\n✓ Reverse batch processor finished")
                    break
                
                for response in batch_responses:
                    self.output_bucket.write(response)
                    print(f"← Stored analysis for batch {response['batch_id']}")
                
                self.llm_queue.task_done()
                
            except Empty:
                if processing_complete.is_set():
                    if self.llm_queue.empty():
                        print("\n✓ Reverse batch processor finished")
                        break
                continue
            except Exception as e:
                print(f"Error in reverse processor: {str(e)}")
                break

class OutputBucket:
    def __init__(self):
        self.storage = []
        self.lock = threading.Lock()
    
    def write(self, data: Dict[str, Any]):
        with self.lock:
            self.storage.append(data)
    
    def read_all(self) -> List[Dict[str, Any]]:
        with self.lock:
            return sorted(self.storage, key=lambda x: (x['batch_id'], x['sentence']))

# Global control flags
shutdown_flag = threading.Event()
processing_complete = threading.Event()

def signal_handler(signum, frame):
    print("\nInterrupt received, shutting down gracefully...")
    shutdown_flag.set()
    processing_complete.set()
    sys.exit(0)

def main():
    signal.signal(signal.SIGINT, signal_handler)
    
    # Initialize components
    llm_response_queue = Queue()
    output_bucket = OutputBucket()
    rate_limiter = RateLimiter(60, llm_response_queue)
    reverse_processor = ReverseBatchProcessor(llm_response_queue, output_bucket)

    # Start reverse processor
    reverse_processor.start()
    
    print("\n Starting sentiment analysis system...")
    
    # Load small dataset for testing
    data = load_dataset('glue', 'sst2')['train'].select(range(6))  # Processing 6 items
    batch_size = 2
    current_batch = []
    batch_id = 0
    
    try:
        for i, example in enumerate(tqdm(data, desc="Reading dataset")):
            if shutdown_flag.is_set():
                break
                
            current_batch.append(example)
            
            if len(current_batch) == batch_size:
                batch = Batch(items=current_batch, batch_id=batch_id)
                if not rate_limiter.process_batch(batch):
                    break
                current_batch = []
                batch_id += 1
        
        # Process remaining items
        if current_batch and not shutdown_flag.is_set():
            batch = Batch(items=current_batch, batch_id=batch_id)
            rate_limiter.process_batch(batch)
        
        # Signal completion and wait for processing to finish
        processing_complete.set()
        llm_response_queue.put(None)  # Signal to reverse processor to finish
        reverse_processor.join()  # Wait for reverse processor to finish
        
        # Print final results
        results = output_bucket.read_all()
        if results:
            print("\nFinal Analysis Results:")
            print("=" * 50)
            for i, result in enumerate(results, 1):
                print(f"\n{i}. Review: {result['sentence'][:100]}...")
                print(f"   Sentiment: {result['analysis']}")
            print("\n=" * 50)
            print(f"Total processed items: {len(results)}")
        else:
            print("\n No results were processed.")
            
    except Exception as e:
        print(f"\n Error in main process: {str(e)}")
        shutdown_flag.set()
    finally:
        print("\n Processing complete!")

if __name__ == "__main__":
    main()

'''
Sample Output: 

Reverse batch processor started...

 Starting sentiment analysis system...
Reading dataset:   0%|                                                                      | 0/6 [00:00<?, ?it/s]
Processing batch 0 with 2 items...
✓ Review analyzed: 'hide new secretions from the parental units ...' → negative
✓ Review analyzed: 'contains no wit , only labored gags ...' → negative
→ Batch 0 sent to processing queue
Reading dataset:  33%|████████████████████▋                                         | 2/6 [00:00<00:01,  2.10it/s]← Stored analysis for batch 0
← Stored analysis for batch 0

Processing batch 1 with 2 items...
✓ Review analyzed: 'that loves its characters and communicates somethi...' → positive
✓ Review analyzed: 'remains utterly satisfied to remain the same throu...' → positive
→ Batch 1 sent to processing queue
Reading dataset:  67%|█████████████████████████████████████████▎                    | 4/6 [00:01<00:00,  2.41it/s]← Stored analysis for batch 1
← Stored analysis for batch 1

Processing batch 2 with 2 items...
✓ Review analyzed: 'on the worst revenge-of-the-nerds clichés the film...' → negative
✓ Review analyzed: 'that 's far too tragic to merit such superficial t...' → negative
→ Batch 2 sent to processing queue
Reading dataset: 100%|██████████████████████████████████████████████████████████████| 6/6 [00:02<00:00,  2.20it/s]
← Stored analysis for batch 2
← Stored analysis for batch 2

✓ Reverse batch processor finished

Final Analysis Results:
==================================================

1. Review: contains no wit , only labored gags ...
   Sentiment: negative

2. Review: hide new secretions from the parental units ...
   Sentiment: negative

3. Review: remains utterly satisfied to remain the same throughout ...
   Sentiment: positive

4. Review: that loves its characters and communicates something rather beautiful about human nature ...
   Sentiment: positive

5. Review: on the worst revenge-of-the-nerds clichés the filmmakers could dredge up ...
   Sentiment: negative

6. Review: that 's far too tragic to merit such superficial treatment ...
   Sentiment: negative

=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
=
Total processed items: 6

'''