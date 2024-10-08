FROM python:3.9-slim
WORKDIR /API
COPY . /API

RUN pip install --no-cache-dir -r requirements.txt

# COPY OPENAI_API_KEY.txt /API/OPENAI_API_KEY.txt

# Expose port for Flask
EXPOSE 5000

# Dont know if we will run this from here
# ENV KAFKA_SERVER=localhost:9092
# ENV KAFKA_TOPIC=llm_requests
# ENV KAFKA_GROUP_ID=llm_group

CMD ["python", "app.py"]
