import functions_framework
from goHandle import goHandle
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
        print(data['User_Project_ID'])
        print(data['User_Dataset_ID'])
        print(data['Input_Table_ID'])
        print(data['Output_Table_ID'])
        print(data['Model'])
        print(data['API_key'])

        jobStatus = goHandle(data['Job_ID'], data['Client_ID'], data['User_Project_ID'],data['User_Dataset_ID'], data['Input_Table_ID'], data['Output_Table_ID'], data['Model'], data['API_key'], )

        # Return a success response
        return jsonify({
            "status": "success",
            "jobStatus": jobStatus
        }), 200

    except Exception as e:
        # Log the error and return an error response
        print(f"Error processing message: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500