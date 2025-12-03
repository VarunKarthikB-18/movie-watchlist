# 🎬 Movie Watchlist

A full-stack web application to organize and manage your personal movie watchlist. Track movies you've watched, rate them, add notes, and plan what to watch next.

## Tech Stack

- **Backend**: Flask 2.3.3, SQLAlchemy 3.0.3, Flask-Migrate 4.0.4, Flask-JWT-Extended 4.4.4
- **Frontend**: Vue 3, Vite, Axios
- **Database**: SQLite (development)
- **Authentication**: JWT (JSON Web Tokens)
- **Styling**: CSS3 with modern gradients and animations

## Project Structure

```
movie-watchlist/
├── backend/
│   ├── app.py                 # Flask app factory, models, and routes
│   ├── requirements.txt       # Python dependencies
│   ├── .env.example           # Environment variables template
│   ├── seeds.py               # Database seeding script
│   ├── migrations/            # Flask-Migrate database migrations
│   └── tests/
│       └── test_basic.py      # Pytest tests
├── frontend/
│   ├── index.html             # HTML entry point
│   ├── vite.config.js         # Vite configuration
│   ├── package.json           # Node dependencies
│   └── src/
│       ├── main.js            # Vue app entry
│       ├── App.vue            # Root component
│       ├── components/        # Vue components
│       │   ├── Login.vue
│       │   ├── Register.vue
│       │   ├── MovieList.vue
│       │   ├── AddMovie.vue
│       │   └── MovieCard.vue
│       └── services/          # API and auth services
│           ├── api.js         # Axios instance with interceptors
│           └── auth.js        # Authentication helpers
├── .gitignore                 # Git ignore rules
└── README.md                  # This file
```

## Local Setup

### Prerequisites

- Python 3.8+
- Node.js 16+ and npm
- SQLite3 (usually pre-installed)

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd movie-watchlist/backend
   ```

2. **Create virtual environment**:
   ```bash
   python3 -m venv venv
   ```

3. **Activate virtual environment**:
   - **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```
   - **Windows**:
     ```bash
     venv\Scripts\activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Set environment variables** (create `.env` file in backend/):
   ```bash
   cp .env.example .env
   # Edit .env and set strong secrets for production
   ```

6. **Initialize database migrations**:
   ```bash
   export FLASK_APP=app:create_app
   export FLASK_ENV=development
   flask db init
   ```

7. **Create initial migration**:
   ```bash
   flask db migrate -m "initial"
   flask db upgrade
   ```

8. **(Optional) Seed sample data**:
   ```bash
   python seeds.py
   ```
   This creates a demo user (email: `demo@example.com`, password: `demo123`) with sample movies.

9. **Run backend**:
   ```bash
   python app.py
   ```
   The backend will be available at `http://127.0.0.1:5000`

### Frontend Setup

1. **In a new terminal, navigate to frontend directory**:
   ```bash
   cd movie-watchlist/frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Start development server**:
   ```bash
   npm run dev
   ```
   The frontend will open at `http://localhost:5173`

4. **Build for production**:
   ```bash
   npm run build
   # Output will be in the `dist/` folder
   ```

## API Endpoints

All endpoints (except `/auth/register` and `/auth/login`) require a valid JWT token in the `Authorization: Bearer <token>` header.

### Authentication

#### Register a new user
```bash
curl -X POST http://127.0.0.1:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123"
  }'
```

**Response (201)**:
```json
{
  "msg": "user created",
  "user_id": 1
}
```

#### Login
```bash
curl -X POST http://127.0.0.1:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123"
  }'
```

**Response (200)**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user_id": 1
}
```

### Movies

#### List all movies (GET /movies)
```bash
TOKEN="your_access_token_here"
curl -X GET http://127.0.0.1:5000/movies \
  -H "Authorization: Bearer $TOKEN"
```

**Response (200)**:
```json
[
  {
    "id": 1,
    "title": "Inception",
    "year": 2010,
    "watched": true,
    "rating": 9,
    "notes": "Mind-bending sci-fi",
    "poster_url": null,
    "user_id": 1
  }
]
```

#### Create a new movie (POST /movies)
```bash
TOKEN="your_access_token_here"
curl -X POST http://127.0.0.1:5000/movies \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "title": "The Matrix",
    "year": 1999,
    "watched": false,
    "rating": null,
    "notes": "Want to rewatch this"
  }'
```

**Response (201)**:
```json
{
  "id": 2,
  "title": "The Matrix",
  "year": 1999,
  "watched": false,
  "rating": null,
  "notes": "Want to rewatch this",
  "poster_url": null,
  "user_id": 1
}
```

#### Update a movie (PUT /movies/<id>)
```bash
TOKEN="your_access_token_here"
curl -X PUT http://127.0.0.1:5000/movies/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "watched": true,
    "rating": 10,
    "notes": "Amazing! Must watch again"
  }'
```

**Response (200)**:
```json
{
  "id": 1,
  "title": "Inception",
  "year": 2010,
  "watched": true,
  "rating": 10,
  "notes": "Amazing! Must watch again",
  "poster_url": null,
  "user_id": 1
}
```

#### Delete a movie (DELETE /movies/<id>)
```bash
TOKEN="your_access_token_here"
curl -X DELETE http://127.0.0.1:5000/movies/1 \
  -H "Authorization: Bearer $TOKEN"
```

**Response (200)**:
```json
{
  "msg": "deleted"
}
```

## Testing

### Run backend tests

From the `backend/` directory:

```bash
# Activate virtual environment first
source venv/bin/activate

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_basic.py

# Run with coverage report
pytest --cov
```

### Manual testing with curl

A complete workflow:

```bash
# 1. Register
curl -X POST http://127.0.0.1:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"testuser@example.com","password":"test123"}'

# 2. Login
TOKEN=$(curl -s -X POST http://127.0.0.1:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"testuser@example.com","password":"test123"}' | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)

# 3. Create a movie
curl -X POST http://127.0.0.1:5000/movies \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{
    "title":"Pulp Fiction",
    "year":1994,
    "watched":true,
    "rating":9
  }'

# 4. List movies
curl http://127.0.0.1:5000/movies \
  -H "Authorization: Bearer $TOKEN"
```

## Deployment

### Backend Deployment

**Heroku** (free tier discontinued, but still a good reference):
1. Install Heroku CLI
2. Create `Procfile` in backend/:
   ```
   web: gunicorn "app:create_app()"
   ```
3. Add production dependencies to `requirements.txt`:
   ```
   gunicorn==21.2.0
   ```
4. Deploy:
   ```bash
   heroku create your-app-name
   heroku config:set SECRET_KEY="your-secret-key"
   heroku config:set JWT_SECRET_KEY="your-jwt-secret"
   git push heroku main
   heroku run flask db upgrade
   ```

**Render/Railway/Fly.io**: Similar process with their respective CLIs and configurations.

### Frontend Deployment

**Netlify**:
```bash
npm run build
# Drag dist/ folder to Netlify or use Netlify CLI
```

**Vercel**:
```bash
npm run build
# Drag dist/ folder to Vercel or use Vercel CLI
```

**GitHub Pages** (static hosting):
```bash
npm run build
# Deploy dist/ to gh-pages branch
```

## Security Considerations

### Development
- Uses SQLite for simplicity (not for production)
- JWT secrets are placeholders (`dev-secret`, `jwt-secret-string`)
- CORS is enabled for all origins (only for local development)

### Production
- **Never commit `.env` file** - use environment variables
- Generate strong JWT secret: `python -c "import secrets; print(secrets.token_hex(32))"`
- Use HTTPS/TLS for all communications
- Use PostgreSQL or MySQL instead of SQLite
- Implement CORS properly (whitelist specific origins)
- Add rate limiting on auth endpoints
- Use strong password requirements
- Enable HTTPS only cookies
- Add CSRF protection if using forms
- Regularly update dependencies: `pip list --outdated`

## Environment Variables

Create `.env` file in `backend/` directory (copy from `.env.example`):

```env
FLASK_APP=app:create_app
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
DATABASE_URL=sqlite:///movies.db
```

## Troubleshooting

### Backend won't start
- Check Python version: `python --version` (need 3.8+)
- Check virtual environment is activated: `which python` should show venv path
- Check all imports: `pip install -r requirements.txt`

### Frontend blank page
- Check browser console for errors (F12)
- Ensure backend is running on `http://127.0.0.1:5000`
- Check CORS is enabled on backend

### Database errors
- Clear database: `rm backend/movies.db` and re-run migrations
- Reset migrations: `rm -rf backend/migrations` and run `flask db init`

### JWT token issues
- Check token format: `Authorization: Bearer <token>` (with space)
- Tokens expire after 24 hours; re-login to get new token
- Check `JWT_SECRET_KEY` matches on backend

## Git & GitHub

### Initial Setup (First Time Only)

```bash
cd movie-watchlist

# Configure git (if not already done)
git config user.name "Your Name"
git config user.email "your.email@example.com"

# Add all files
git add .

# Initial commit
git commit -m "feat: initial movie watchlist app scaffold"

# Add GitHub remote (replace USERNAME with your GitHub username)
git remote add origin https://github.com/VarunKarthikB-18/movie-watchlist.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### Making Changes

```bash
# Create a feature branch
git checkout -b feature/your-feature

# Make your changes, then commit
git add .
git commit -m "feat: add feature description"

# Push to GitHub
git push origin feature/your-feature

# Create a pull request on GitHub
```

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -m "feat: add feature"`
4. Push to branch: `git push origin feature/your-feature`
5. Open a pull request

## License

MIT License - feel free to use this project for learning and personal projects.

## GitHub Repository

**Repository**: https://github.com/VarunKarthikB-18/movie-watchlist

## Support

For issues and questions:
- Check existing GitHub issues
- Create a new GitHub issue with detailed description
- Include backend logs and browser console errors
- Tag issues appropriately (bug, feature, documentation)
