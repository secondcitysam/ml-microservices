from flask import jsonify


def register_routes(app):

    @app.route("/", methods=["GET"])
    def home():
        return jsonify({
            "service": "Data Processing Service",
            "message": "Data Processing Service is running"
        }), 200

    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({
            "service": "data-processing",
            "status": "healthy"
        }), 200
