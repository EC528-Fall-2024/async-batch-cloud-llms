'''Flask App to run in background in Cloud'''
from flask import Flask
import threading

app = Flask(__name__)

@app.route("/")
def health_check():
    return "Running", 200

def run_flask():
    app.run(host="0.0.0.0", port=8080)