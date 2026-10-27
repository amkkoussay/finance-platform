from flask import Flask, jsonify
from flask_cors import CORS

from config import Config
from models import db


def create_app(config_object=Config):
    """Application factory — lets tests spin up an isolated app instance."""
    app = Flask(__name__)
    app.config.from_object(config_object)

    # SECRET_KEY must come from the environment. The old "dev-key" fallback
    # let anyone forge a valid JWT (the key was public in this repo), so a
    # missing key is a startup failure, not a silent default — except in
    # tests, where TestConfig already sets its own key.
    if not app.config.get("SECRET_KEY"):
        if app.config.get("TESTING"):
            app.config["SECRET_KEY"] = "test-only-secret"
        else:
            raise RuntimeError(
                "SECRET_KEY is not set. Set SECRET_KEY in the environment "
                "or in a backend/.env file before starting the app "
                "(see backend/.env.example for the format)."
            )

    # Enable CORS so the React frontend (different port) can call this API
    CORS(app)

    # Initialize SQLAlchemy database
    db.init_app(app)

    # Register blueprints
    from routes.auth import bp as auth_bp
    from routes.transactions import bp as transactions_bp
    from routes.analytics import bp as analytics_bp
    from routes.categories import bp as categories_bp
    from routes.predictions import bp as predictions_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(transactions_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(categories_bp)
    app.register_blueprint(predictions_bp)

    @app.route("/", methods=["GET"])
    def index():
        """Simple health-check route to confirm the backend is running."""
        return jsonify({"message": "Backend working"})

    return app


def __getattr__(name):
    """Build the module-level app lazily.

    Importing this module (e.g. the test suite importing create_app) must
    not fail when SECRET_KEY is unset; any real use of ``app`` still goes
    through create_app() and fails loudly, as above.
    """
    if name == "app":
        return create_app()
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
