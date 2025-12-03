import os
from datetime import timedelta
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    JWTManager, create_access_token, jwt_required, get_jwt_identity
)

# ----- Extensions -----
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # App Config
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///movies.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # JWT config (must be set before registering jwt-protected routes)
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "jwt-secret-string")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)  # Enable CORS for frontend communication
    JWTManager(app)

    @app.route('/')
    def home():
        return jsonify({"message": "Movie Watchlist backend is running!"})

    # ---------- AUTH ----------
    @app.route('/auth/register', methods=['POST'])
    def register():
        data = request.get_json() or {}
        email = data.get('email')
        password = data.get('password')
        if not email or not password:
            return {"msg": "email and password required"}, 400
        if User.query.filter_by(email=email).first():
            return {"msg": "email already registered"}, 400
        hashed = generate_password_hash(password)
        user = User(email=email, password=hashed)
        db.session.add(user)
        db.session.commit()
        return {"msg": "user created", "user_id": user.id}, 201

    @app.route('/auth/login', methods=['POST'])
    def login():
        data = request.get_json() or {}
        email = data.get('email')
        password = data.get('password')
        if not email or not password:
            return {"msg":"email and password required"}, 400
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            return {"msg":"bad credentials"}, 401
        access_token = create_access_token(identity=user.id)
        return {"access_token": access_token, "user_id": user.id}, 200

    # ---------- MOVIE CRUD (protected) ----------
    @app.route('/movies', methods=['GET'])
    @jwt_required()
    def list_movies():
        # Retrieve the logged-in user ID from the JWT token
        user_id = get_jwt_identity()
        # Fetch all movies for this user, ordered by newest first
        movies = Movie.query.filter_by(user_id=user_id).order_by(Movie.id.desc()).all()
        return jsonify([m.to_dict() for m in movies]), 200

    @app.route('/movies', methods=['POST'])
    @jwt_required()
    def create_movie():
        # Get user ID from JWT token
        user_id = get_jwt_identity()
        data = request.get_json() or {}
        title = data.get('title')
        if not title:
            return jsonify({"msg": "title required"}), 400
        # Create movie with optional fields
        movie = Movie(
            title=title,
            year=data.get('year'),
            watched=bool(data.get('watched', False)),
            rating=data.get('rating'),
            notes=data.get('notes'),
            poster_url=data.get('poster_url'),
            user_id=user_id
        )
        db.session.add(movie)
        db.session.commit()
        return jsonify(movie.to_dict()), 201

    @app.route('/movies/<int:movie_id>', methods=['PUT'])
    @jwt_required()
    def update_movie(movie_id):
        # Only allow user to update their own movies
        user_id = get_jwt_identity()
        movie = Movie.query.filter_by(id=movie_id, user_id=user_id).first()
        if not movie:
            return jsonify({"msg":"movie not found"}), 404
        data = request.get_json() or {}
        # Update allowed fields
        for key in ('title','year','watched','rating','notes','poster_url'):
            if key in data:
                setattr(movie, key, data.get(key))
        db.session.commit()
        return jsonify(movie.to_dict()), 200

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @jwt_required()
    def delete_movie(movie_id):
        # Only allow user to delete their own movies
        user_id = get_jwt_identity()
        movie = Movie.query.filter_by(id=movie_id, user_id=user_id).first()
        if not movie:
            return jsonify({"msg":"movie not found"}), 404
        db.session.delete(movie)
        db.session.commit()
        return jsonify({"msg":"deleted"}), 200

    return app


# ---------- MODELS ----------
class User(db.Model):
    """User model: stores email and hashed password"""
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    # Relationship to Movie model
    movies = db.relationship("Movie", backref="user", lazy=True)

    def to_dict(self):
        """Convert User to dictionary"""
        return {"id": self.id, "email": self.email}


class Movie(db.Model):
    """Movie model: stores movie data and links to User"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    year = db.Column(db.Integer)
    watched = db.Column(db.Boolean, default=False)
    rating = db.Column(db.Integer)
    notes = db.Column(db.Text)
    poster_url = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def to_dict(self):
        """Convert Movie to dictionary"""
        return {
            "id": self.id,
            "title": self.title,
            "year": self.year,
            "watched": bool(self.watched),
            "rating": self.rating,
            "notes": self.notes,
            "poster_url": self.poster_url,
            "user_id": self.user_id
        }


if __name__ == "__main__":
    # For local run: use create_app() and run with Flask development server
    app = create_app()
    app.run(debug=True)
