from flask import Flask, jsonify
from flask_cors import CORS

from config import Config
from models import db


def create_app(config_object=Config):
    """Application factory — lets tests spin up an isolated app instance."""
    app = Flask(__name__)
    app.config.from_object(config_object)

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


app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
