"""
Seed script to populate the database with sample data
Run this after migrations: python seeds.py
"""
from app import create_app, db, User, Movie
from werkzeug.security import generate_password_hash


def seed_data():
    """Create sample user and movies"""
    app = create_app()
    
    with app.app_context():
        # Clear existing data (optional)
        # db.drop_all()
        # db.create_all()
        
        # Check if sample user already exists
        if User.query.filter_by(email="demo@example.com").first():
            print("Sample data already exists!")
            return
        
        # Create sample user
        user = User(
            email="demo@example.com",
            password=generate_password_hash("demo123")
        )
        db.session.add(user)
        db.session.commit()
        print(f"✓ Created user: demo@example.com (password: demo123)")
        
        # Create sample movies
        movies = [
            Movie(
                title="Inception",
                year=2010,
                watched=True,
                rating=9,
                notes="Mind-bending sci-fi masterpiece",
                user_id=user.id
            ),
            Movie(
                title="The Shawshank Redemption",
                year=1994,
                watched=True,
                rating=10,
                notes="Classic drama about hope and friendship",
                user_id=user.id
            ),
            Movie(
                title="Interstellar",
                year=2014,
                watched=True,
                rating=9,
                notes="Epic space exploration film",
                user_id=user.id
            ),
            Movie(
                title="Dune",
                year=2021,
                watched=False,
                rating=None,
                notes="Want to watch the newest adaptation",
                user_id=user.id
            ),
        ]
        
        db.session.add_all(movies)
        db.session.commit()
        print(f"✓ Created {len(movies)} sample movies")
        print("\nSample data loaded successfully!")
        print("\nYou can now login with:")
        print("  Email: demo@example.com")
        print("  Password: demo123")


if __name__ == "__main__":
    seed_data()
