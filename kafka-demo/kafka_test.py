from kafka import KafkaProducer, KafkaConsumer
from kafka.errors import KafkaError

# Set up the producer
producer = KafkaProducer(bootstrap_servers=['localhost:9093'])

# Produce a message
def produce_message(topic, message):
    try:
        future = producer.send(topic, message.encode('utf-8'))
        result = future.get(timeout=10)
        print(f'Message sent: {result}')
    except KafkaError as e:
        print(f'Failed to send message: {e}')

# Set up the consumer
consumer = KafkaConsumer(
    'test_topic',
    bootstrap_servers=['localhost:9093'],
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='my-group')

# Consume messages
def consume_messages():
    for message in consumer:
        print(f'Message received: {message.value.decode("utf-8")}')

# Main execution
if __name__ == '__main__':
    topic = 'test_topic'
    message = 'Hello, Kafka!'

    produce_message(topic, message)
    consume_messages()
