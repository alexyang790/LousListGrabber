from flask import Blueprint, jsonify, render_template, request
from app.services import fetch_data_service, search_data_service, display_sample_data, get_csv_service

# Create a blueprint for routes
routes = Blueprint("routes", __name__)

@routes.route('/')
def home():
    return jsonify({'message': "Lou's List App is Running!"})

@routes.route('/fetch')
def fetch_data():
    return fetch_data_service()

@routes.route('/data')
def display_data():
    return display_sample_data()

@routes.route('/GetCSV')
def get_csv():
    return get_csv_service()

@routes.route('/search/<query>')
def search_data(query):
    return search_data_service(query)

# Function to initialize routes in the app
def init_routes(app):
    app.register_blueprint(routes)

