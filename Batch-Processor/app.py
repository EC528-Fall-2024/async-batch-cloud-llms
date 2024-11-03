from flask import Flask, request, jsonify
from test_table_reader import query_bigquery
from testSinglePubSubSender import pubSubSender


app = Flask(__name__)

# Home route with a simple GET request
@app.route("/", methods=["GET"])
def home():
    return "Welcome to the Flask API!"

# A POST route that echoes back the JSON data received
@app.route("/runjob", methods=["POST"])
def run_job():
    data = request.get_json()  # Parse JSON data from request body
    result = query_bigquery(2)
    pubSubSender(result)

    return jsonify({"received_data": data}), 200

# Run the app
if __name__ == "__main__":
    app.run(port=5004, debug=True)