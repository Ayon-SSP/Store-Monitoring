import json
import uuid
from flask import Flask, jsonify, request, send_file

app = Flask(__name__)

empty_reports_json = {
    "queue": []
}
with open('report_status.json', 'w') as f:
    json.dump(empty_reports_json, f)


# Define the trigger_report endpoint
@app.route('/trigger_report', methods=['GET'])
def trigger_report():
    """Trigger a report generation and return the report ID"""
    report_id = str(uuid.uuid4())

    with open('report_status.json', 'r') as f:
        reports_json = json.load(f)

    reports_json["queue"].append(report_id)
    reports_json[report_id] = {'status': 'Running'}

    with open('report_status.json', 'w') as f:
        json.dump(reports_json, f)

    return jsonify({'report_id': report_id})

# Define the get_report endpoint
@app.route('/get_report', methods=['GET'])
def get_report():
    """Get the status of a report generation and return the status"""

    report_id = request.json['report_id']

    with open('report_status.json', 'r') as f:
        reports_json = json.load(f)

    # Check if the report ID is valid
    if report_id not in reports_json['queue']:
        return jsonify({'error': 'Invalid report ID'})

    if is_report_complete(report_id):
        return jsonify({'status': 'Complete', 'csv': get_csv(report_id)})
    else:
        return jsonify({'status': 'Running'})

@app.route('/download/<report_id>', methods=['GET', 'POST'])
def download_file(report_id):
    """Download the CSV file"""
    file_path = f'res/{report_id}.csv'
    return send_file(file_path, as_attachment=True)

# Function to check if the report generation is complete
def is_report_complete(report_id):
    """Check if the report generation is complete"""

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
    """Get the CSV file"""
    return f'Download the csv file from /download/{report_id}'

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
