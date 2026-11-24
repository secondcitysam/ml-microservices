
from flask import jsonify, request
import numpy as np


# Iris classification labels
CLASS_NAMES = {
    0: "setosa",
    1: "versicolor",
    2: "virginica"
}


def validate_features(data):
    """
    Validate the incoming processed feature vector.
    """

    if not isinstance(data, dict):
        raise ValueError(
            "Request must be a JSON object"
        )

    if "feature_vector" not in data:
        raise ValueError(
            "Request must contain feature_vector"
        )

    features = data["feature_vector"]

    if not isinstance(features, list):
        raise ValueError(
            "feature_vector must be a list"
        )

    if len(features) != 4:
        raise ValueError(
            "Exactly 4 features are required"
        )

    processed_features = []

    for value in features:

        if value is None or isinstance(value, bool):
            raise ValueError(
                "Feature values must be numeric"
            )

        try:
            value = float(value)

        except (TypeError, ValueError):
            raise ValueError(
                "Feature values must be numeric"
            )

        if not np.isfinite(value) or value <= 0:
            raise ValueError(
                "Feature values must be finite positive numbers"
            )

        processed_features.append(value)

    return processed_features


def register_routes(app):

    # Home endpoint
    @app.route("/", methods=["GET"])
    def home():

        return jsonify({
            "service": "Prediction Service",
            "message": "Prediction Service is running"
        }), 200

    # Health check endpoint
    @app.route("/health", methods=["GET"])
    def health():

        model_loaded = (
            app.config.get("ML_MODEL") is not None
        )

        return jsonify({
            "service": "prediction",
            "status": "healthy" if model_loaded else "unhealthy",
            "model_loaded": model_loaded
        }), 200 if model_loaded else 503

    # Prediction endpoint
    @app.route("/predict", methods=["POST"])
    def predict():

        try:

            # Step 1: Receive JSON request
            data = request.get_json(silent=True)

            # Step 2: Validate feature vector
            features = validate_features(data)

            # Step 3: Retrieve loaded ML model
            model = app.config["ML_MODEL"]

            # Step 4: Convert features into NumPy array
            input_data = np.array(
                [features],
                dtype=float
            )

            # Step 5: Generate prediction
            prediction = int(
                model.predict(input_data)[0]
            )

            # Step 6: Generate class probabilities
            probabilities = model.predict_proba(
                input_data
            )[0]

            probability_result = {}

            for class_id, probability in zip(
                model.classes_,
                probabilities
            ):

                class_id = int(class_id)

                probability_result[
                    CLASS_NAMES[class_id]
                ] = round(float(probability), 4)

            # Step 7: Return prediction response
            return jsonify({
                "success": True,
                "prediction": {
                    "class_id": prediction,
                    "species": CLASS_NAMES[prediction],
                    "probabilities": probability_result
                }
            }), 200

        except ValueError as error:

            return jsonify({
                "success": False,
                "error": str(error)
            }), 400

        except Exception:

            app.logger.exception(
                "Unexpected error during prediction"
            )

            return jsonify({
                "success": False,
                "error": "Internal server error"
            }), 500
