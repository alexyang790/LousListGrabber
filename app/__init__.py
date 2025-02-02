from flask import Flask
from flasgger import Swagger
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Initialize Swagger
    Swagger(app)

    # Register routes
    from app.routes import init_routes
    init_routes(app)

    return app