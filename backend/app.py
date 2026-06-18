"""LeadFlow Flask application scaffold.

Phase 1 intentionally avoids route registration and business behavior.
"""

from flask import Flask

from config import Config


def create_app(config_class: type[Config] = Config) -> Flask:
    """Create the Flask application shell.

    TODO: Register blueprints, extensions, error handlers, and middleware in a later phase.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    return app


app = create_app()


if __name__ == "__main__":
    # TODO: Replace with production-ready server entrypoint in deployment phase.
    app.run(debug=True)

