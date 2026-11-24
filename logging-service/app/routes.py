from flask import jsonify


def register_routes(app):

    @app.route("/", methods=["GET"])
    def home():
        return jsonify({
            "service": "Logging Service",
            "message": "Logging Service is running"
        }), 200

    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({
            "service": "logging",
            "status": "healthy"
        }), 200
