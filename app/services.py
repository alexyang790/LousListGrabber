import requests
import pandas as pd
from flask import jsonify, send_file
import json

def get_headers():
    url = 'http://httpbin.org/user-agent'
    try:
        r = requests.get(url)
        r.raise_for_status()  # Raise an HTTPError for bad responses
        myjson = r.json()
        useragent = myjson.get('user-agent', 'default-user-agent')
        return {'User-Agent': useragent}
    except requests.exceptions.RequestException as e:
        print(f"Error fetching headers: {e}")
        return None

def fetch_data_service():
    url = 'https://louslist.org/deliverData.php'
    form_data = {
        "Group": "CS",
        "Semester": "1252",
        "Extended": "Yes",
    }
    headers = get_headers()
    if not headers:
        return jsonify({"error": "Failed to fetch headers"}), 500

    try:
        response = requests.post(url, data=form_data, headers=headers)
        response.raise_for_status()

        # Save the data as a CSV file
        file_name = 'data/data.csv'
        with open(file_name, 'wb') as f:
            f.write(response.content)

        return jsonify({"message": f"Data fetched successfully and saved as {file_name}"})
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return jsonify({"error": "Error fetching data"}), 500
    except Exception as e:
        print(f"Unexpected error: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

def display_sample_data():
    try:
        file_name = 'data/data.csv'
        data = pd.read_csv(file_name)
        sample_data = data.head().to_dict(orient='records')
        return jsonify({"message": "Data loaded successfully!", "data": sample_data})
    except FileNotFoundError:
        return jsonify({"error": "No data found. Please fetch data first!"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
def get_csv_service():
    try:
        file_name = 'data.csv'
        return send_file(file_name, as_attachment=True)
    except FileNotFoundError:
        return jsonify({"error": "No data found. Please fetch data first!"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def search_data_service(query):
    try:
        if not query:
            return jsonify({"error": "Query parameter is required."}), 400

        # Load the CSV file
        file_name = 'data/data.csv'
        data = pd.read_csv(file_name)

        # Perform a case-insensitive search across all columns
        results = data.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)
        matching_data = data[results]

        # Replace NaN with None (JSON `null`)
        matching_data = matching_data.where(pd.notnull(matching_data), None)

        # Convert the results to JSON
        matching_data_json = matching_data.to_dict(orient='records')

        if matching_data_json:
            return jsonify({"results": matching_data_json})
        else:
            return jsonify({"message": "No matching results found."})

    except FileNotFoundError:
        return jsonify({"error": "No data found. Please fetch data first!"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500