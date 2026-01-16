#!/bin/bash

echo "🚀 AI Incident Commander - Quick Start"
echo "======================================="
echo ""

# Check if setup was run
if [ ! -d "backend/venv" ]; then
    echo "⚠️  Setup not detected. Running setup first..."
    echo ""
    bash setup.sh
    if [ $? -ne 0 ]; then
        echo "❌ Setup failed. Please check the errors above."
        exit 1
    fi
    echo ""
fi

# Load demo data if needed
echo "📊 Checking demo data..."
cd backend
source venv/bin/activate

# Check if data already loaded (check for incidents)
python -c "from app.db.storage import storage; print(len(storage.incidents))" 2>/dev/null | grep -q "^0$"
if [ $? -eq 0 ]; then
    echo "Loading demo incidents..."
    python seed_data.py
fi

cd ..

echo ""
echo "✅ Starting AI Incident Commander..."
echo ""
echo "📝 This will open 2 terminals:"
echo "   1. Backend API server (http://localhost:8000)"
echo "   2. Frontend web app (http://localhost:3000)"
echo ""
echo "Press Ctrl+C in both terminals to stop"
echo ""
echo "Starting in 3 seconds..."
sleep 3

# Start backend in background
echo ""
echo "🐍 Starting backend..."
cd backend
source venv/bin/activate
python run.py &
BACKEND_PID=$!
cd ..

# Wait for backend to start
echo "⏳ Waiting for backend to start..."
sleep 5

# Start frontend
echo ""
echo "⚛️  Starting frontend..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "========================================="
echo "✅ AI Incident Commander is running!"
echo "========================================="
echo ""
echo "🌐 Frontend: http://localhost:3000"
echo "📡 Backend:  http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/api/docs"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Wait for Ctrl+C
trap "echo ''; echo 'Stopping services...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; echo 'Stopped!'; exit" INT

wait
