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

def search_data_service(query, return_format=None):
    try:
        file_name = os.path.join(os.getcwd(), 'data.csv')
        data = pd.read_csv(file_name)

        # Perform a case-insensitive search across all columns
        results = data.apply(
            lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)
        matching_data = data[results]

        if matching_data.empty:
            return jsonify({"results": []}), 200

        if return_format == 'csv':
            # Return CSV file for download
            csv_io = io.StringIO()
            matching_data.to_csv(csv_io, index=False)
            csv_io.seek(0)
            return send_file(
                io.BytesIO(csv_io.getvalue().encode('utf-8')),
                mimetype='text/csv',
                as_attachment=True,
                download_name='search_results.csv'
            )

        # Replace NaN values with None for JSON compatibility
        matching_data = matching_data.where(pd.notnull(matching_data), None)

        if return_format == 'json':
            # Convert DataFrame to JSON and return
            return jsonify({"results": matching_data.to_dict(orient='records')}), 200

        # Default to JSON (remove NaN values as well)
        return jsonify({"results": matching_data.to_dict(orient='records')}), 200

    except FileNotFoundError:
        return jsonify({"error": "Data not found. Please fetch it first."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500