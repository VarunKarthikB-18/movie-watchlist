# 🚀 Next Steps to Run Movie Watchlist

## Quick Start (5 minutes)

Follow these steps to get the application running locally.

### Step 1: Backend Setup

Open **Terminal 1** and run:

```bash
# Navigate to backend directory
cd /Users/bvksmacbook/Documents/movie-watchlist/backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Set up environment (copy template)
cp .env.example .env

# Initialize database migrations
export FLASK_APP=app:create_app
export FLASK_ENV=development

# Create and run migrations
flask db migrate -m "initial"
flask db upgrade

# (Optional) Load sample data
python seeds.py
# Creates demo user: email=demo@example.com, password=demo123

# Start backend server
python app.py
```

**Expected output:**
```
 * Running on http://127.0.0.1:5000 (Press CTRL+C to quit)
```

### Step 2: Frontend Setup

Open **Terminal 2** (keep Terminal 1 running) and run:

```bash
# Navigate to frontend directory
cd /Users/bvksmacbook/Documents/movie-watchlist/frontend

# Install Node dependencies
npm install

# Start development server
npm run dev
```

**Expected output:**
```
  VITE v4.4.9  ready in 123 ms

  ➜  Local:   http://localhost:5173/
  ➜  press h to show help
```

### Step 3: Access Application

1. **Automatically opens** in your browser at `http://localhost:5173`
2. If not, manually navigate to that URL
3. Register a new account or login with:
   - Email: `demo@example.com`
   - Password: `demo123`

---

## Verify Everything Works

### Test Backend API (Terminal 3)

```bash
# Test health check
curl http://127.0.0.1:5000/

# Register new user
curl -X POST http://127.0.0.1:5000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123"}'

# Login and get token
TOKEN=$(curl -s -X POST http://127.0.0.1:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123"}' | grep -o '"access_token":"[^"]*"' | cut -d'"' -f4)

# Create a movie
curl -X POST http://127.0.0.1:5000/movies \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"title":"Inception","year":2010,"watched":true,"rating":9}'

# List movies
curl http://127.0.0.1:5000/movies \
  -H "Authorization: Bearer $TOKEN" | jq
```

### Test Frontend UI

1. Go to `http://localhost:5173` in your browser
2. Register or login
3. Add a new movie
4. Toggle "watched" status
5. Delete a movie

---

## Project File Structure

```
movie-watchlist/
├── README.md                    # Full documentation
├── setup.sh                     # Automated setup script (optional)
├── requirements.txt             # Python dependencies (root reference)
├── .gitignore                   # Git ignore rules
│
├── backend/
│   ├── app.py                   # Flask app, models, and all routes
│   ├── requirements.txt         # Python package versions
│   ├── seeds.py                 # Sample data seeding script
│   ├── .env.example             # Environment variables template
│   ├── .gitignore               # Backend-specific ignores
│   ├── migrations/              # Flask-Migrate database migrations
│   │   ├── env.py
│   │   ├── script.py.mako
│   │   └── versions/
│   │       └── 81a5440f715a_.py
│   └── tests/
│       └── test_basic.py        # Pytest test suite
│
└── frontend/
    ├── package.json             # Node.js dependencies
    ├── vite.config.js           # Vite configuration
    ├── index.html               # HTML entry point
    └── src/
        ├── main.js              # Vue app initialization
        ├── App.vue              # Root Vue component
        ├── components/
        │   ├── Login.vue        # Login form component
        │   ├── Register.vue     # Registration form component
        │   ├── MovieList.vue    # Movie list display
        │   ├── AddMovie.vue     # Add movie form
        │   └── MovieCard.vue    # Individual movie card
        └── services/
            ├── api.js           # Axios instance + interceptors
            └── auth.js          # Auth utilities (login, logout, token)
```

---

## Backend Endpoints Cheatsheet

| Method | Endpoint | Auth Required | Purpose |
|--------|----------|---------------|---------|
| POST | `/auth/register` | ❌ No | Create new user |
| POST | `/auth/login` | ❌ No | Get JWT token |
| GET | `/movies` | ✅ Yes | List user's movies |
| POST | `/movies` | ✅ Yes | Create new movie |
| PUT | `/movies/<id>` | ✅ Yes | Update movie |
| DELETE | `/movies/<id>` | ✅ Yes | Delete movie |

---

## Running Tests

```bash
# Navigate to backend directory
cd backend
source venv/bin/activate

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test
pytest tests/test_basic.py::test_login_success -v

# Generate coverage report
pytest --cov=. --cov-report=html
```

---

## Development Features

### Auto-reload
- **Backend**: Flask auto-reloads on code changes (debug mode)
- **Frontend**: Vite provides hot module replacement (HMR)

### Database
- SQLite database stored in `backend/movies.db`
- Clear database: `rm backend/movies.db && flask db upgrade`

### Debugging
- **Backend**: Add `print()` statements or use Python debugger
- **Frontend**: Browser DevTools (F12)

---

## Common Issues & Solutions

### Issue: "ModuleNotFoundError: No module named 'flask'"
**Solution**: Activate virtual environment
```bash
cd backend
source venv/bin/activate
```

### Issue: "Cannot find module 'vue'"
**Solution**: Install Node dependencies
```bash
cd frontend
npm install
```

### Issue: Backend returns 401 "Unauthorized"
**Solution**: JWT token expired or invalid. Re-login to get new token.

### Issue: Frontend blank page
**Solution**: Check browser console (F12). Ensure backend is running.

### Issue: CORS errors in browser console
**Solution**: Verify backend is running on `http://127.0.0.1:5000`

### Issue: "Address already in use" for port 5000
**Solution**: Backend already running. Kill existing process:
```bash
lsof -ti:5000 | xargs kill -9
```

---

## Production Deployment Checklist

- [ ] Change `FLASK_ENV` to `production`
- [ ] Generate strong `SECRET_KEY`: `python -c "import secrets; print(secrets.token_hex(32))"`
- [ ] Generate strong `JWT_SECRET_KEY`: `python -c "import secrets; print(secrets.token_hex(32))"`
- [ ] Use PostgreSQL/MySQL instead of SQLite
- [ ] Set `CORS_ORIGINS` to specific frontend domain
- [ ] Enable HTTPS/TLS
- [ ] Run `npm run build` for frontend
- [ ] Use production WSGI server (Gunicorn, uWSGI)
- [ ] Set up environment variables in deployment platform
- [ ] Run database migrations on production
- [ ] Set up monitoring and error tracking

---

## Helpful Commands

```bash
# Backend
cd backend
source venv/bin/activate              # Activate venv
pip install -r requirements.txt       # Install dependencies
pip list --outdated                   # Check for updates
flask db migrate -m "description"     # Create new migration
flask db upgrade                      # Apply migrations
flask db downgrade                    # Revert last migration
python seeds.py                       # Load sample data
pytest -v                             # Run tests

# Frontend
cd frontend
npm install                           # Install dependencies
npm run dev                           # Start dev server
npm run build                         # Build for production
npm update                            # Update dependencies
npm outdated                          # Check for updates

# Git
git add .                             # Stage all changes
git commit -m "feat: description"     # Commit changes
git push origin main                  # Push to GitHub
```

---

## Environment Variables

**Backend `.env` file** (create from `.env.example`):
```env
FLASK_APP=app:create_app
FLASK_ENV=development
SECRET_KEY=your-secret-key-here (change in production!)
JWT_SECRET_KEY=your-jwt-secret-here (change in production!)
DATABASE_URL=sqlite:///movies.db
```

**Frontend** (uses `http://127.0.0.1:5000` by default):
Edit `frontend/src/services/api.js` to change API URL.

---

## Learning Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/)
- [Vue 3 Guide](https://vuejs.org/guide/introduction.html)
- [Vite Documentation](https://vitejs.dev/)
- [Axios Documentation](https://axios-http.com/)

---

## Support & Troubleshooting

1. **Check README.md** for comprehensive documentation
2. **Check browser console** (F12) for frontend errors
3. **Check terminal output** for backend errors
4. **Review code comments** in `app.py` and Vue components
5. **Run tests** to validate functionality

---

## Next: Push to GitHub

When ready to share your code:

```bash
cd /Users/bvksmacbook/Documents/movie-watchlist

# Initialize git (if not already)
git init

# Add all files
git add .

# Create initial commit
git commit -m "feat: complete movie watchlist app"

# Add remote and push
git remote add origin https://github.com/VarunKarthikB-18/movie-watchlist.git
git branch -M main
git push -u origin main
```

**Happy coding! 🎬**
