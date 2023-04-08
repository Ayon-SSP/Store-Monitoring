import json
from flask import Flask, jsonify, request
import uuid

app = Flask(__name__)


empty_reports_json = {
    "queue": []
}
with open('report_status.json', 'w') as f:
    json.dump(empty_reports_json, f)


# Define the trigger_report endpoint
@app.route('/trigger_report', methods=['GET'])
def trigger_report():
    # Generate a unique report ID
    report_id = str(uuid.uuid4())

    with open('report_status.json', 'r') as f:
        reports_json = json.load(f)

    reports_json["queue"].append(report_id)
    reports_json[report_id] = {'status': 'Running'}

    with open('report_status.json', 'w') as f:
        json.dump(reports_json, f)

    # Return the report ID as JSON
    return jsonify({'report_id': report_id})

# Define the get_report endpoint
@app.route('/get_report', methods=['GET'])
def get_report():
    # Get the report ID from the request
    # report_id = request.args.get('report_id')
    report_id = request.json['report_id']

    with open('report_status.json', 'r') as f:
        reports_json = json.load(f)

    # Check if the report ID is valid
    if report_id not in reports_json['queue']:
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
    # Return True if the report generation is complete, else False

    with open('report_status.json', 'r') as f:
        reports_json = json.load(f)
    if reports_json[report_id]['status'] == 'Complete':
        with open('report_status.json', 'r') as f:
            reports_json = json.load(f)

        reports_json["queue"].remove(report_id)
        del reports_json[report_id]

        with open('report_status.json', 'w') as f:
            json.dump(reports_json, f)
        return True
    else:
        return False

# Function to get the CSV file
def get_csv(report_id):
    # Your code to get the CSV file goes here
    # script to download csv file in the browser using flask where the file is in the res/<report_id>.csv
    return 'Download the csv file'

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
