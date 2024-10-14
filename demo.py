from flask import Flask


app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, Cloud Run!'  


@app.route('/json')
def json_response():
    return {"message": "Hello, this is a JSON response"}


if __name__ == '__main__':
    import os
    
    port = int(os.environ.get("PORT", 8080))
    
    app.run(host='0.0.0.0', port=port)
