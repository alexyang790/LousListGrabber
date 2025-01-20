from flask import Flask
from flasgger import Swagger

def create_app():
    app = Flask(__name__)

    # Initialize Swagger
    Swagger(app)

    # Register routes
    from app.routes import init_routes
    init_routes(app)

    return app