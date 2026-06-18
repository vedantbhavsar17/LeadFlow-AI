"""LeadFlow Flask application scaffold.

Phase 1 intentionally avoids route registration and business behavior.
"""

from flask import Flask

from config import Config
from database.extensions import init_database


def create_app(config_class: type[Config] = Config) -> Flask:
    """Create the Flask application shell.

    TODO: Register blueprints, error handlers, and middleware in a later phase.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    init_database(app)
    return app


app = create_app()


if __name__ == "__main__":
    # TODO: Replace with production-ready server entrypoint in deployment phase.
    app.run(debug=True)
