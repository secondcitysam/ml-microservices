
from flask import jsonify, request
from datetime import datetime, timezone
import math


# Expected feature order for the Iris ML model
FEATURE_ORDER = [
    "sepal_length",
    "sepal_width",
    "petal_length",
    "petal_width"
]


def validate_and_process(data):
    """
    Validate and preprocess incoming Iris flower data.
    """

    # Step 1: Validate request structure
    if not isinstance(data, dict) or "features" not in data:
        raise ValueError(
            "Request must contain a 'features' object"
        )

    features = data["features"]

    if not isinstance(features, dict):
        raise ValueError(
            "'features' must be a JSON object"
        )

    # Step 2: Check for missing features
    missing_features = [
        feature
        for feature in FEATURE_ORDER
        if feature not in features
    ]

    if missing_features:
        raise ValueError(
            f"Missing required features: {missing_features}"
        )

    # Step 3: Check for unexpected features
    unexpected_features = [
        feature
        for feature in features
        if feature not in FEATURE_ORDER
    ]

    if unexpected_features:
        raise ValueError(
            f"Unexpected features: {unexpected_features}"
        )

    processed_features = {}

    # Step 4: Validate and clean feature values
    for feature in FEATURE_ORDER:

        value = features[feature]

        if value is None or isinstance(value, bool):
            raise ValueError(
                f"Invalid value for {feature}"
            )

        try:
            value = float(value)

        except (TypeError, ValueError):
            raise ValueError(
                f"{feature} must be numeric"
            )

        if not math.isfinite(value) or value <= 0:
            raise ValueError(
                f"{feature} must be a finite positive number"
            )

        processed_features[feature] = value

    # Step 5: Arrange features in the expected ML model order
    feature_vector = [
        processed_features[feature]
        for feature in FEATURE_ORDER
    ]

    # Step 6: Return processed data
    return {
        "features": processed_features,
        "feature_vector": feature_vector,
        "feature_count": len(feature_vector),
        "processed_at": datetime.now(
            timezone.utc
        ).isoformat()
    }


def register_routes(app):

    # Home endpoint
    @app.route("/", methods=["GET"])
    def home():

        return jsonify({
            "service": "Data Processing Service",
            "message": "Data Processing Service is running"
        }), 200

    # Health check endpoint
    @app.route("/health", methods=["GET"])
    def health():

        return jsonify({
            "service": "data-processing",
            "status": "healthy"
        }), 200

    # Data processing endpoint
    @app.route("/process", methods=["POST"])
    def process_data():

        try:
            data = request.get_json()

            processed_data = validate_and_process(data)

            return jsonify({
                "success": True,
                "message": "Data processed successfully",
                "data": processed_data
            }), 200

        except ValueError as error:

            return jsonify({
                "success": False,
                "error": str(error)
            }), 400

        except Exception:

            app.logger.exception(
                "Unexpected error during data processing"
            )

            return jsonify({
                "success": False,
                "error": "Internal server error"
            }), 500
