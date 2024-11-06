import json
import socket
import random
import time

from confluent_kafka import Producer
from faker import Faker
from datetime import datetime

fake = Faker()

# Function for generating an example job
def generate_job():
    user = fake.simple_profile()

    return {
        "jobId": fake.uuid4(),
        "userId": user['username'],
        "jobDate": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "message": fake.paragraph(nb_sentences=5)
    }

# Function for producer callback
def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
    else:
        print("Message produced: %s" % (str(msg)))

def main():
    # Create producer
    conf = {'.bootstrapservers': 'localhost:9092',
        'client.id': socket.gethostname()}
    producer = Producer(conf)
    topic = 'inbound-data'

    curr_time = datetime.now()

    while (datetime.now() - curr_time).seconds < 120:
        try:
            # Generate job
            job = generate_job()
            print(job)

            # Send example data to 'inbound-data' topic
            producer.produce(topic, key=job['jobId'], value=json.dumps(job), callback=acked)
            producer.poll(0)

            # Wait 5 seconds
            time.sleep(5)
        except BufferError:
            print("Buffer full! Waiting...")
            time.sleep(1)
        except Exception as e:
            print(e)

if __name__ == "__main__":
    main()