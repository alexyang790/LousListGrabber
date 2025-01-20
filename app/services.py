import requests
import pandas as pd
from flask import jsonify, send_file
import json
import os
import io 

def fetch_data_service():
    try:
        # URL to fetch data
        url = 'https://louslist.org/deliverData.php'
        form_data = {
            "Group": "CS",
            "Semester": "1252",
            "Extended": "Yes",
        }

        # Fetch the data
        response = requests.post(url, data=form_data)
        response.raise_for_status()  # Raise an error for HTTP errors

        # Read the CSV data into a DataFrame
        df = pd.read_csv(io.StringIO(response.text))

        # Store the DataFrame into a CSV file
        csv_file_path = os.path.join(os.getcwd(), 'data.csv')  # Unified file name
        df.to_csv(csv_file_path, index=False)

        # Return a success message
        return jsonify({"message": "Data fetched and stored successfully", "file_path": csv_file_path}), 200

    except requests.exceptions.RequestException as e:
        # Handle request-related exceptions
        return jsonify({"error": f"Failed to fetch data due to network issue: {str(e)}"}), 500
    except pd.errors.ParserError as e:
        # Handle errors in parsing the CSV
        return jsonify({"error": f"Failed to parse the fetched data: {str(e)}"}), 500
    except Exception as e:
        # Catch-all for other exceptions
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

def display_sample_data():
    try:
        # Dynamically determine the file path
        file_name = os.path.join(os.getcwd(), 'data.csv')

        # Check if the file exists
        if not os.path.exists(file_name):
            raise FileNotFoundError("The data.csv file does not exist. Please use /fetch first")

        # Read the CSV file into a DataFrame
        data = pd.read_csv(file_name)

        # Replace NaN values with None for JSON compatibility
        data = data.where(pd.notnull(data), None)

        # Convert the DataFrame to JSON format
        data_json = data.to_dict(orient='records')

        # Return the JSON response
        return jsonify({"data": data_json})

    except FileNotFoundError:
        return jsonify({"error": "No data found. Please fetch data first!"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
def get_csv_service():
    try:
        file_name = os.path.join(os.getcwd(), 'data.csv')
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
        file_name = os.path.join(os.getcwd(), 'data.csv')
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