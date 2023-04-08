"""
## API requirement

1. You need two APIs
    1. /trigger_report endpoint that will trigger report generation from the data provided (stored in DB)
        1. No input
        2. Output - report_id (random string)
        3. report_id will be used for polling the status of report completion
    2. /get_report endpoint that will return the status of the report or the csv
        1. Input - report_id
        2. Output
            - if report generation is not complete, return “Running” as the output
            - if report generation is complete, return “Complete” along with the CSV file with the schema described above.
"""


import time
from flask import Flask, jsonify, request
import uuid

app = Flask(__name__)

# Define the database to store data
database = []
# Define the trigger_report endpoint
@app.route('/trigger_report', methods=['GET'])
def trigger_report():
    # Generate a unique report ID
    report_id = str(uuid.uuid4())

    # Store the report ID in the database
    database.append(report_id)

    print(database)
    # Return the report ID as JSON
    return jsonify({'report_id': report_id})

# Define the get_report endpoint
@app.route('/get_report', methods=['GET'])
def get_report():
    # Get the report ID from the request
    # report_id = request.args.get('report_id')
    report_id = request.json['report_id']

    # Check if the report ID is valid
    if report_id not in database:
        return jsonify({'error': 'Invalid report ID'})

    # Check if the report generation is complete
    # If not, return "Running"
    # If complete, return "Complete" along with the CSV file
    if is_report_complete(report_id):
        return jsonify({'status': 'Complete', 'csv': get_csv(report_id)})
    else:
        return jsonify({'status': 'Running'})

# Function to check if the report generation is complete
def is_report_complete(report_id):
    # Your code to check if the report generation is complete goes here
    # Return True if the report generation is complete, else False
    # sleep for 20 seconds
    time.sleep(20)
    return True

# Function to get the CSV file
def get_csv(report_id):
    # Your code to get the CSV file goes here
    # Return the CSV file as a string
    return 'CSV file'

# Run the Flask app
if __name__ == '__main__':
    app.run()
