'''Rate-Limiting Module Main'''
import threading
from app import run_flask
from init import init_limiters
from Subscriber import batch_receiver

if __name__ == "__main__":
    threading.Thread(target=run_flask).start() # Start Flask API
    if not init_limiters(): # Initialize rate-limiters
        print("Failed to initialize limiters")
        quit()
    batch_receiver() # Start receiving messages from batch processor