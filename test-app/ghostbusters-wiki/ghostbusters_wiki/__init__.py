import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Use env var if provided; fallback to your local setup
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL",
        "postgresql://peter_venkman:ghost@localhost:5432/ghostbusters",
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    Migrate(app, db)

    # Must be imported after db is initialized to avoid circular imports
    # Consider a better way to handle this
    from .models.ghost import Ghost

    @app.route('/ghosts')
    def getGhosts():
        ghosts = Ghost.query.all()
        return jsonify([{"id": f.id, "name": f.name} for f in ghosts])

    return app