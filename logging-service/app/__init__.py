
from flask import Flask

from app.storage import initialize_storage


def create_app():

    app = Flask(__name__)

    # Initialize log storage
    initialize_storage()

    # Register REST API routes
    from app.routes import register_routes

    register_routes(app)

    return app
