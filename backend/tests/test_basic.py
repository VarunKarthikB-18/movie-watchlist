"""
Basic pytest tests for Movie Watchlist backend
Tests register, login, and movie CRUD endpoints
"""
import pytest
import json
from app import create_app, db, User, Movie


@pytest.fixture
def app():
    """Create and configure a test app instance"""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """A test client for the app"""
    return app.test_client()


def test_home(client):
    """Test home endpoint returns success message"""
    resp = client.get('/')
    assert resp.status_code == 200
    data = json.loads(resp.data)
    assert "Movie Watchlist backend is running" in data["message"]


def test_register_success(client):
    """Test user registration with valid email and password"""
    resp = client.post('/auth/register', 
        json={"email": "test@example.com", "password": "pass123"})
    assert resp.status_code == 201
    data = json.loads(resp.data)
    assert data["msg"] == "user created"
    assert data["user_id"] == 1


def test_register_missing_fields(client):
    """Test registration fails without email or password"""
    resp = client.post('/auth/register', json={"email": "test@example.com"})
    assert resp.status_code == 400
    data = json.loads(resp.data)
    assert "required" in data["msg"]


def test_register_duplicate_email(client):
    """Test registration fails if email already exists"""
    client.post('/auth/register', 
        json={"email": "test@example.com", "password": "pass123"})
    resp = client.post('/auth/register', 
        json={"email": "test@example.com", "password": "pass456"})
    assert resp.status_code == 400
    data = json.loads(resp.data)
    assert "already registered" in data["msg"]


def test_login_success(client):
    """Test successful login returns JWT token"""
    client.post('/auth/register', 
        json={"email": "test@example.com", "password": "pass123"})
    resp = client.post('/auth/login', 
        json={"email": "test@example.com", "password": "pass123"})
    assert resp.status_code == 200
    data = json.loads(resp.data)
    assert "access_token" in data
    assert data["user_id"] == 1


def test_login_bad_credentials(client):
    """Test login fails with wrong password"""
    client.post('/auth/register', 
        json={"email": "test@example.com", "password": "pass123"})
    resp = client.post('/auth/login', 
        json={"email": "test@example.com", "password": "wrongpass"})
    assert resp.status_code == 401
    data = json.loads(resp.data)
    assert "bad credentials" in data["msg"]


def test_login_nonexistent_user(client):
    """Test login fails for non-existent user"""
    resp = client.post('/auth/login', 
        json={"email": "nope@example.com", "password": "pass123"})
    assert resp.status_code == 401


def test_create_movie_protected(client):
    """Test that creating movie requires authentication"""
    resp = client.post('/movies', json={"title": "Inception"})
    assert resp.status_code == 401


def test_create_movie_success(client):
    """Test successful movie creation with valid token"""
    # Register and login
    client.post('/auth/register', 
        json={"email": "test@example.com", "password": "pass123"})
    login_resp = client.post('/auth/login', 
        json={"email": "test@example.com", "password": "pass123"})
    token = json.loads(login_resp.data)["access_token"]
    
    # Create movie with token
    headers = {"Authorization": f"Bearer {token}"}
    resp = client.post('/movies', 
        json={"title": "Inception", "year": 2010, "rating": 9},
        headers=headers)
    assert resp.status_code == 201
    data = json.loads(resp.data)
    assert data["title"] == "Inception"
    assert data["year"] == 2010
    assert data["rating"] == 9


def test_create_movie_missing_title(client):
    """Test movie creation fails without title"""
    client.post('/auth/register', 
        json={"email": "test@example.com", "password": "pass123"})
    login_resp = client.post('/auth/login', 
        json={"email": "test@example.com", "password": "pass123"})
    token = json.loads(login_resp.data)["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    resp = client.post('/movies', 
        json={"year": 2010},
        headers=headers)
    assert resp.status_code == 400


def test_list_movies(client):
    """Test listing movies for authenticated user"""
    # Setup: register, login, create movie
    client.post('/auth/register', 
        json={"email": "test@example.com", "password": "pass123"})
    login_resp = client.post('/auth/login', 
        json={"email": "test@example.com", "password": "pass123"})
    token = json.loads(login_resp.data)["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    client.post('/movies', 
        json={"title": "Inception", "year": 2010},
        headers=headers)
    
    # List movies
    resp = client.get('/movies', headers=headers)
    assert resp.status_code == 200
    data = json.loads(resp.data)
    assert len(data) == 1
    assert data[0]["title"] == "Inception"


def test_update_movie(client):
    """Test updating a movie"""
    # Setup: register, login, create movie
    client.post('/auth/register', 
        json={"email": "test@example.com", "password": "pass123"})
    login_resp = client.post('/auth/login', 
        json={"email": "test@example.com", "password": "pass123"})
    token = json.loads(login_resp.data)["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    create_resp = client.post('/movies', 
        json={"title": "Inception", "watched": False},
        headers=headers)
    movie_id = json.loads(create_resp.data)["id"]
    
    # Update movie
    resp = client.put(f'/movies/{movie_id}', 
        json={"watched": True},
        headers=headers)
    assert resp.status_code == 200
    data = json.loads(resp.data)
    assert data["watched"] is True


def test_delete_movie(client):
    """Test deleting a movie"""
    # Setup: register, login, create movie
    client.post('/auth/register', 
        json={"email": "test@example.com", "password": "pass123"})
    login_resp = client.post('/auth/login', 
        json={"email": "test@example.com", "password": "pass123"})
    token = json.loads(login_resp.data)["access_token"]
    
    headers = {"Authorization": f"Bearer {token}"}
    create_resp = client.post('/movies', 
        json={"title": "Inception"},
        headers=headers)
    movie_id = json.loads(create_resp.data)["id"]
    
    # Delete movie
    resp = client.delete(f'/movies/{movie_id}', headers=headers)
    assert resp.status_code == 200
    
    # Verify it's deleted
    list_resp = client.get('/movies', headers=headers)
    data = json.loads(list_resp.data)
    assert len(data) == 0
