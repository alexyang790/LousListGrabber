from flask import Blueprint, jsonify, request
from app.services import fetch_data_service, search_data_service, display_sample_data, get_csv_service
from flasgger import Swagger, swag_from

# Create a blueprint for routes
routes = Blueprint("routes", __name__)

@routes.route('/')
def home():
    """
    Welcome Route
    ---
    responses:
      200:
        description: Returns a welcome message
    """
    return jsonify({'message': "Lou's List App is Running!"})

@routes.route('/fetch')
@swag_from({
    'responses': {
        200: {
            'description': 'Fetch data from Lous List and save it as a CSV file.'
        },
        500: {
            'description': 'Failed to fetch data or save the file.'
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
            'description': 'CSV file not found. Fetch data first.'
        }
    }
})
def display_data():
    return display_sample_data()

@routes.route('/getcsv')
@swag_from({
    'responses': {
        200: {
            'description': 'Download the CSV file.',
            'content': {
                'text/csv': {}
            }
        },
        404: {
            'description': 'CSV file not found. Fetch data first.'
        }
    }
})
def get_csv():
    return get_csv_service()

@routes.route('/search/<query>')
@swag_from({
    'parameters': [
        {
            'name': 'query',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'Search query to filter the CSV data.'
        }
    ],
    'responses': {
        200: {
            'description': 'Search results as JSON.',
            'content': {
                'application/json': {
                    'example': {
                        'results': [
                            {'column1': 'value1', 'column2': 'value2'}
                        ]
                    }
                }
            }
        },
        404: {
            'description': 'CSV file not found. Fetch data first.'
        }
    }
})
def search_data(query):
    return search_data_service(query)

# Function to initialize routes in the app
def init_routes(app):
    app.register_blueprint(routes)