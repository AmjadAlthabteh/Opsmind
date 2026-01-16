#!/bin/bash

echo "🚀 AI Incident Commander - Setup Script"
echo "========================================"
echo ""

# Check Python version
echo "📋 Checking Python version..."
python_version=$(python3 --version 2>&1 | grep -oP '\d+\.\d+')
if (( $(echo "$python_version >= 3.11" | bc -l) )); then
    echo "✅ Python $python_version detected"
else
    echo "❌ Python 3.11+ required. Please install Python 3.11 or higher."
    exit 1
fi

# Check Node.js version
echo ""
echo "📋 Checking Node.js version..."
if command -v node &> /dev/null; then
    node_version=$(node --version | grep -oP '\d+' | head -1)
    if [ "$node_version" -ge 18 ]; then
        echo "✅ Node.js $(node --version) detected"
    else
        echo "❌ Node.js 18+ required. Please install Node.js 18 or higher."
        exit 1
    fi
else
    echo "❌ Node.js not found. Please install Node.js 18 or higher."
    exit 1
fi

# Setup backend
echo ""
echo "🐍 Setting up backend..."
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Create .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo ""
    echo "⚠️  IMPORTANT: Edit backend/.env and add your OPENAI_API_KEY"
    echo "   (Optional - AI features will work in demo mode without it)"
fi

cd ..

# Setup frontend
echo ""
echo "⚛️  Setting up frontend..."
cd frontend

# Install dependencies
echo "Installing Node.js dependencies..."
npm install

cd ..

echo ""
echo "✅ Setup complete!"
echo ""
echo "🎯 Next steps:"
echo ""
echo "1. (Optional) Add your OpenAI API key to backend/.env"
echo "   Without it, the system runs with demo AI responses"
echo ""
echo "2. Load demo data:"
echo "   cd backend && python seed_data.py"
echo ""
echo "3. Start the servers (in separate terminals):"
echo "   Terminal 1: cd backend && python run.py"
echo "   Terminal 2: cd frontend && npm run dev"
echo ""
echo "4. Open http://localhost:3000 in your browser"
echo ""
echo "📚 For more info, see README.md"
echo ""
