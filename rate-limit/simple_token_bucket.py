from kafka import KafkaProducer, KafkaConsumer
import time

# Simple Token bucket implementation
class TokenBucket:
    def __init__(self, capacity, refill_rate):
        self.capacity = capacity
        self.refill_rate = refill_rate
        self.tokens = capacity
        self.last_refill = time.time()

    def refill(self):
        now = time.time()
        tokens_to_add = (now - self.last_refill) * self.refill_rate
        self.tokens = min(self.capacity, self.tokens + tokens_to_add)
        self.last_refill = now

    def consume(self, num_tokens):
        self.refill() # refill every consumption
        if self.tokens >= num_tokens:
            self.tokens -= num_tokens
            return True
        return False

# ------------------- Will test this once Kafka working ---------------------
# def produce_messages(producer):
#     for i in range(10):
#         message = f"message {i}"
#         producer.send('test_topic', message.encode())
#         print(f"sent: {message}")
#         time.sleep(0.5)  # delay between messages

# # kafka setup
# producer = KafkaProducer(bootstrap_servers='kafka:9092')
# consumer = KafkaConsumer('test_topic', bootstrap_servers='kafka:9092', group_id='group1')

# # kafka produces 10 messages to consumer
# produce_messages(producer)
# -----------------------------------------------------------------------

# Temporary code to test token bucket
def produce_messages():
    messages = [f"message {i}" for i in range(10)]
    for message in messages:
        yield message
        time.sleep(0.5)  # simulate delay between message production


# Init bucket w 10 token capacity, 1 token refill rate
bucket = TokenBucket(10, 1)

# Messages from consumer try to consume token from bucket
for message in produce_messages():
    if bucket.consume(1):  # attempt consumption of token
        print(f"Processing message: {message}")
    else:
        print("Rate limit exceeded, waiting for tokens...")
        time.sleep(1)  # replacement for exponential backoff
