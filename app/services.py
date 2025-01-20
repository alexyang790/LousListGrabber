import requests
import pandas as pd
from flask import jsonify

def fetch_data_service():
    url = 'https://louslist.org/deliverData.php'
    form_data = {
        "Group": "CS",
        "Semester": "1252",
        "Extended": "Yes",
    }

    try:
        response = requests.post(url, data=form_data)
        response.raise_for_status()

        # Save the data as a CSV file
        file_name = 'data/data.csv'
        with open(file_name, 'wb') as f:
            f.write(response.content)

        return jsonify({"message": f"Data fetched successfully and saved as {file_name}"})
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

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

def search_data_service(query):
    try:
        if not query:
            return jsonify({"error": "Query parameter is required."}), 400

        file_name = 'data/data.csv'
        data = pd.read_csv(file_name)
        results = data.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)
        matching_data = data[results].to_dict(orient='records')

        return jsonify({"results": matching_data}) if matching_data else jsonify({"message": "No matching results found."})
    except FileNotFoundError:
        return jsonify({"error": "No data found. Please fetch data first!"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500