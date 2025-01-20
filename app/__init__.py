from flask import Flask
from app.routes import init_routes

def create_app():
    app = Flask(__name__)

    # Register routes
    from app.routes import init_routes
    init_routes(app)

    return app