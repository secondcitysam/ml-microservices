from flask import jsonify


def register_routes(app):

    @app.route("/", methods=["GET"])
    def home():
        return jsonify({
            "service": "Prediction Service",
            "message": "Prediction Service is running"
        }), 200

    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({
            "service": "prediction",
            "status": "healthy"
        }), 200
