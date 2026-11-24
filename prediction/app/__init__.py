
import os
import joblib
from flask import Flask


def create_app():

    app = Flask(__name__)

    # Locate the prediction service directory
    base_dir = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )

    # Locate the trained ML model
    model_path = os.path.join(
        base_dir,
        "model",
        "iris_model.joblib"
    )

    # Check whether model exists
    if not os.path.exists(model_path):
        raise FileNotFoundError(
            f"Trained model not found: {model_path}. "
            "Run train_model.py first."
        )

    # Load the model once during application startup
    model = joblib.load(model_path)

    # Store model in Flask application configuration
    app.config["ML_MODEL"] = model

    # Register API routes
    from app.routes import register_routes

    register_routes(app)

    return app
