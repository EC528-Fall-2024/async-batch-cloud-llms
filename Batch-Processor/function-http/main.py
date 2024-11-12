import base64
import functions_framework
from handleGo import handleGo
from flask import request, jsonify

# Triggered by an HTTP request
@functions_framework.http
def go(request):
    try:
        # Parse JSON payload from the HTTP request
        request_json = request.get_json()

        data = request.get_json()  # Parse JSON data from request body
        print(data['Job_ID'])
        print(data['Client_ID'])
        # print(data['Database_Length'])


        # Call the handleGo function (database length is hardcoded here as 13)
        jobStatus = handleGo(data['Job_ID'], data['Client_ID'], 13)

        # Return a success response
        return jsonify({
            "status": "success",
            "jobStatus": jobStatus
        }), 200

    except Exception as e:
        # Log the error and return an error response
        print(f"Error processing message: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500