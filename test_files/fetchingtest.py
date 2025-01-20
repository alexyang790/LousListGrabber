import requests
import json

def get_headers():
    url = 'http://httpbin.org/user-agent'
    response = requests.get(url)
    response.raise_for_status()  # Ensure the request was successful
    myjson = response.json()  # Use .json() to parse JSON directly
    useragent = myjson['user-agent']
    return {'User-Agent': useragent}

# Get headers
headers = get_headers()

# Target URL and form data
url = 'https://louslist.org/deliverData.php'
form_data = {
    "Group": "CS",
    "Semester": "1252",
    "Extended": "Yes",
}

# Make POST request
response = requests.post(url, data=form_data, headers=headers)

# Handle the response
if response.ok:
    try:
        myjson = response.json()  # Parse JSON response
        print(myjson)
    except json.JSONDecodeError:
        print("Response is not valid JSON:", response.text)
else:
    print(f"Request failed with status code {response.status_code}: {response.text}")