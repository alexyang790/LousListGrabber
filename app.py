# imports
from flask import Flask, jsonify, render_template, request
import requests
import json 
import pandas as pd

# Get Headers
def getheaders():
    global headers
    url = 'http://httpbin.org/user-agent'
    r = requests.get(url)
    myjson = json.loads(r.text)
    useragent = myjson['user-agent']
    headers = {'User-Agent': useragent}

app = Flask(__name__)

# Test route
@app.route('/')
def home():
    return jsonify({'message': "Lou's List App is Running!"})

# Fetch Route
@app.route('/fetch')
def fetch_data():
    # URL to send the POST request
    url = 'https://louslist.org/deliverData.php'

    # Form data (mimicking the form submission)
    form_data = {
        "Group": "CS",
        "Semester": "1252",
        "Extended": "Yes",  # Include Additional Class Meetings
        # Add other options like "Description" or "InstructionMode" if needed
    }

    try:
        # Send the POST request
        response = requests.post(url, data=form_data)
        response.raise_for_status()  # Raise an error if the request fails

        # Save the data as a CSV file
        file_name = 'data.csv'
        with open(file_name, 'wb') as f:
            f.write(response.content)

        return jsonify({"message": f"Data fetched successfully and saved as {file_name}"})

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/data')
def display_data():
    try:
        # Load the data from the saved CSV
        file_name = 'data.csv'
        data = pd.read_csv(file_name)

        # Convert the first few rows to JSON
        sample_data = data.head().to_dict(orient='records')

        return jsonify({"message": "Data loaded successfully!", "data": sample_data})

    except FileNotFoundError:
        return jsonify({"error": "No data found. Please fetch data first!"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/search/<query>')
def search_data(query):
    try:
        # Load the data
        file_name = 'data.csv'
        data = pd.read_csv(file_name)

        # Perform a case-insensitive search across all columns
        results = data.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)

        # Convert the matching rows to JSON
        matching_data = data[results].to_dict(orient='records')

        if matching_data:
            return jsonify({"message": f"Found {len(matching_data)} matching results.", "results": matching_data})
        else:
            return jsonify({"message": "No matching results found."})

    except FileNotFoundError:
        return jsonify({"error": "No data found. Please fetch data first!"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/dashboard', methods=['GET'])
def dashboard():
    query = request.args.get('query')
    results = None

    if query:
        try:
            file_name = 'data.csv'
            data = pd.read_csv(file_name)

            # Perform search
            matches = data.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)
            results = data[matches].to_dict(orient='records')

        except FileNotFoundError:
            return render_template('dashboard.html', error="No data found. Please fetch data first!")
        except Exception as e:
            return render_template('dashboard.html', error=str(e))

    return render_template('dashboard.html', results=results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)