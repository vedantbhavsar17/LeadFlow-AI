"""LeadFlow Flask application scaffold.

Phase 1 intentionally avoids route registration and business behavior.
"""

from typing import Any

from flask import Flask

from api import register_api
from config import Config
from database.extensions import init_database


def create_app(config_class: type[Config] = Config, config_overrides: dict[str, Any] | None = None) -> Flask:
    """Create the Flask application shell.

    TODO: Register middleware in a later phase.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    if config_overrides:
        app.config.update(config_overrides)
    init_database(app)
    register_api(app)
    return app


app = create_app()


if __name__ == "__main__":
    # TODO: Replace with production-ready server entrypoint in deployment phase.
    app.run(debug=True)
