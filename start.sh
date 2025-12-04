#!/bin/bash

# Function to kill processes on exit
cleanup() {
    echo "Stopping servers..."
    kill $(jobs -p) 2>/dev/null
    exit
}

trap cleanup SIGINT SIGTERM

echo "🚀 Starting Movie Watchlist..."

# Start Backend
echo "Starting Backend (Python/Flask)..."
cd backend
if [ -d "venv" ]; then
    source venv/bin/activate
fi
# Check if requirements are installed (basic check)
if ! pip freeze | grep -q Flask; then
    echo "Installing backend dependencies..."
    pip install -r requirements.txt
fi
python3 app.py &
BACKEND_PID=$!
cd ..

# Wait a moment for backend to initialize
sleep 2

# Start Frontend
echo "Starting Frontend (Vite)..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo "✅ Servers are running!"
echo "Backend: http://localhost:5001"
echo "Frontend: http://localhost:5173"
echo "Press Ctrl+C to stop both servers."

wait
