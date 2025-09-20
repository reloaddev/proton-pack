from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        'postgresql://sw:sw@localhost:5432/starwars'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    Migrate(app, db)

    # Must be imported after db is initialized to avoid circular imports
    # Consider a better way to handle this
    from .models.star_fighter import StarFighter

    @app.route('/star-fighters')
    def star_fighters():
        fighters = StarFighter.query.all()
        return jsonify([{"id": f.id, "name": f.name} for f in fighters])
    return app