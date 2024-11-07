from flask import Flask, request, jsonify
from handleGo import handleGo

app = Flask(__name__)

# Home route with a simple GET request
@app.route("/test", methods=["GET"])
def home():
    return "Welcome to the Flask API!"


@app.route("/go", methods=["POST"])
def go():
    data = request.get_json()  # Parse JSON data from request body
    print(data['Job_ID'])
    print(data['Client_ID'])
    print(data['Database_Length'])

    
    # Call Function to haldle go
    jobStatus = handleGo(data['Job_ID'], data['Client_ID'], data['Database_Length'])
        
    if(jobStatus):
        responseMessage = {"Job_Status": "Started"}
    else:
        responseMessage = {"error": "Error_message"}

    return jsonify(responseMessage), 200


    

# Run the app
if __name__ == "__main__":
    app.run(port=8080, debug=True)
    
    
    
