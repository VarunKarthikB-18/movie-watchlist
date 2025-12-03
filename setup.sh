#!/bin/bash
# Movie Watchlist - Quick Setup Script
# Run this script to set up the entire project locally

set -e  # Exit on error

echo "🎬 Movie Watchlist - Development Setup"
echo "======================================"
echo ""

# Check Python version
echo "📦 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "   Python version: $python_version"

# Check Node version
echo "📦 Checking Node version..."
node_version=$(node --version)
npm_version=$(npm --version)
echo "   Node version: $node_version"
echo "   npm version: $npm_version"

echo ""
echo "📁 Setting up Backend..."
echo "------------------------"

# Navigate to backend
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Set environment variables
echo ""
echo "🔐 Setting up environment variables..."
if [ ! -f ".env" ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "   ⚠️  Please edit backend/.env and set strong SECRET_KEY and JWT_SECRET_KEY"
else
    echo "   ✓ .env already exists"
fi

# Initialize database
echo ""
echo "🗄️  Setting up database..."
export FLASK_APP=app:create_app
export FLASK_ENV=development

if [ ! -d "migrations/versions" ] || [ -z "$(ls -A migrations/versions)" ]; then
    echo "Initializing migrations..."
    flask db migrate -m "initial"
fi

echo "Upgrading database..."
flask db upgrade

# Seed sample data
echo ""
echo "🌱 Seeding sample data..."
echo "   (demo@example.com / demo123)"
python seeds.py

echo ""
echo "✓ Backend setup complete!"
echo ""

# Navigate to frontend
cd ../frontend

echo "📁 Setting up Frontend..."
echo "------------------------"

# Install Node dependencies
echo "Installing Node dependencies..."
npm install

echo ""
echo "✓ Frontend setup complete!"
echo ""

# Final instructions
echo "🚀 Setup Complete!"
echo "==================="
echo ""
echo "To run the application:"
echo ""
echo "Terminal 1 - Backend:"
echo "  $ cd backend"
echo "  $ source venv/bin/activate  (or venv\\Scripts\\activate on Windows)"
echo "  $ python app.py"
echo "  Backend runs on: http://127.0.0.1:5000"
echo ""
echo "Terminal 2 - Frontend:"
echo "  $ cd frontend"
echo "  $ npm run dev"
echo "  Frontend runs on: http://localhost:5173"
echo ""
echo "Demo credentials:"
echo "  Email: demo@example.com"
echo "  Password: demo123"
echo ""
echo "For more information, see README.md"
