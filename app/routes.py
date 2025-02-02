from flask import Blueprint, jsonify, request, render_template
from app.services import fetch_data_service, search_data_service, display_sample_data, get_csv_service, advanced_search_service
from flasgger import swag_from

# Create a blueprint for routes
routes = Blueprint("routes", __name__)

@routes.route('/')
@swag_from({
    'responses': {
        200: {
            'description': 'Returns a welcome message'
        }
    }
})
def home():
    return jsonify({'message': "Lou's List App is Running!"})

@routes.route('/fetch')
@swag_from({
    'responses': {
        200: {
            'description': 'Fetch data from Lou\'s List and save it as a CSV file.',
        },
        500: {
            'description': 'Failed to fetch data or save the file.',
        }
    }
})
def fetch_data():
    return fetch_data_service()

@routes.route('/data')
@swag_from({
    'responses': {
        200: {
            'description': 'Display the entire CSV data as JSON.',
            'content': {
                'application/json': {
                    'example': {
                        'data': [
                            {'column1': 'value1', 'column2': 'value2'}
                        ]
                    }
                }
            }
        },
        404: {
            'description': 'CSV file not found. Fetch data first.',
        }
    }
})
def display_data():
    return display_sample_data()

@routes.route('/getcsv')
@swag_from({
    'responses': {
        200: {
            'description': 'Download the entire CSV file.',
        },
        404: {
            'description': 'CSV file not found. Fetch data first.',
        }
    }
})
def get_csv():
    return get_csv_service()

@routes.route('/search/<query>/<return_format>')
@swag_from({
    'parameters': [
        {
            'name': 'query',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'Search query to filter the CSV data.'
        },
        {
            'name': 'return_format',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': "Response format: 'json' or 'csv'."
        }
    ],
    'responses': {
        200: {
            'description': 'Search results in the specified format.',
        },
        404: {
            'description': 'CSV file not found. Fetch data first.',
        }
    }
})
def search_data(query, return_format):
    return search_data_service(query, return_format)

@routes.route('/dashboard')
@swag_from({
    'responses': {
        200: {
            'description': 'Render the dashboard HTML page for user interaction.',
        }
    }
})
def dashboard():
    return render_template('dashboard.html')

@routes.route('/advanced_search/ofs/<query>/<return_format>')
@swag_from({
    'parameters': [
        {
            'name': 'query',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'Search query for OFS-specific columns.'
        },
        {
            'name': 'return_format',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': "Response format: 'json' or 'csv'."
        }
    ],
    'responses': {
        200: {
            'description': 'Filtered results for OFS-specific columns in the specified format.',
        },
        404: {
            'description': 'No matching results found or data file not available.',
        }
    }
})
def advanced_search_ofs(query, return_format):
    return advanced_search_service(query, columns=['ClassNumber', 'Room1', 'Days1', 'Enrollment', 'MeetingDates1', 'Type'], return_format=return_format)

@routes.route('/advanced_search/enrollment/<query>/<return_format>')
@swag_from({
    'parameters': [
        {
            'name': 'query',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'Search query for Enrollment-specific columns.'
        },
        {
            'name': 'return_format',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': "Response format: 'json' or 'csv'."
        }
    ],
    'responses': {
        200: {
            'description': 'Filtered results for Enrollment-specific columns in the specified format.',
        },
        404: {
            'description': 'No matching results found or data file not available.',
        }
    }
})
def advanced_search_enrollment(query, return_format):
    return advanced_search_service(query, columns=['ClassNumber', 'Days1', 'Enrollment', 'EnrollmentLimit', 'Status', 'Title'], return_format=return_format)

# Function to initialize routes in the app
def init_routes(app):
    app.register_blueprint(routes)