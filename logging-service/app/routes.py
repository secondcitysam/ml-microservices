
from flask import jsonify, request
from datetime import datetime, timezone

from app.storage import save_log, get_logs


# Supported logging levels
VALID_LEVELS = [
    "DEBUG",
    "INFO",
    "WARNING",
    "ERROR",
    "CRITICAL"
]


def validate_log(data):
    """
    Validate incoming log information.
    """

    if not isinstance(data, dict):
        raise ValueError(
            "Request must be a JSON object"
        )

    # Validate service name
    service = data.get("service")

    if not isinstance(service, str) or not service.strip():
        raise ValueError(
            "A valid service name is required"
        )

    # Validate log level
    level = data.get("level", "INFO")

    if not isinstance(level, str):
        raise ValueError(
            "Log level must be a string"
        )

    level = level.upper().strip()

    if level not in VALID_LEVELS:
        raise ValueError(
            f"Invalid log level. Allowed: {VALID_LEVELS}"
        )

    # Validate message
    message = data.get("message")

    if not isinstance(message, str) or not message.strip():
        raise ValueError(
            "A valid log message is required"
        )

    # Validate metadata
    metadata = data.get("metadata", {})

    if not isinstance(metadata, dict):
        raise ValueError(
            "Metadata must be a JSON object"
        )

    return {
        "timestamp": datetime.now(
            timezone.utc
        ).isoformat(),

        "service": service.strip(),

        "level": level,

        "message": message.strip(),

        "metadata": metadata
    }


def register_routes(app):

    # Home endpoint
    @app.route("/", methods=["GET"])
    def home():

        return jsonify({
            "service": "Logging Service",
            "message": "Logging Service is running"
        }), 200

    # Health check endpoint
    @app.route("/health", methods=["GET"])
    def health():

        return jsonify({
            "service": "logging-service",
            "status": "healthy"
        }), 200

    # Receive and store logs
    @app.route("/logs", methods=["POST"])
    def create_log():

        try:

            data = request.get_json(silent=True)

            # Validate incoming log
            log_entry = validate_log(data)

            # Store log record
            save_log(log_entry)

            return jsonify({
                "success": True,
                "message": "Log stored successfully",
                "log": log_entry
            }), 201

        except ValueError as error:

            return jsonify({
                "success": False,
                "error": str(error)
            }), 400

        except Exception:

            app.logger.exception(
                "Unexpected error while storing log"
            )

            return jsonify({
                "success": False,
                "error": "Internal server error"
            }), 500

    # Retrieve stored logs
    @app.route("/logs", methods=["GET"])
    def retrieve_logs():

        try:

            limit = request.args.get(
                "limit",
                default=100,
                type=int
            )

            if limit is None or limit < 1 or limit > 1000:
                return jsonify({
                    "success": False,
                    "error": "Limit must be between 1 and 1000"
                }), 400

            logs = get_logs(limit)

            return jsonify({
                "success": True,
                "total_logs": len(logs),
                "logs": logs
            }), 200

        except Exception:

            app.logger.exception(
                "Unexpected error while retrieving logs"
            )

            return jsonify({
                "success": False,
                "error": "Internal server error"
            }), 500
