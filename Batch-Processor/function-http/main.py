import functions_framework
from handleGo import handleGo
from flask import jsonify

# Triggered by an HTTP request
@functions_framework.http
def go(request):
    try:
        # Parse JSON payload from the HTTP request
        request_json = request.get_json()
        data = request.get_json()  # Parse JSON data from request body
        print(data['Job_ID'])
        print(data['Client_ID'])
        
        # Can uncomment when we are ready
        
        # print(data['Project_ID'])
        # print(data['Database_ID'])
        # print(data['Input_Table_ID'])
        # print(data['Output_Table_ID'])
        # print(data['Model'])
        
        # print(data['Database_Length'])

        # Call the handleGo function
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