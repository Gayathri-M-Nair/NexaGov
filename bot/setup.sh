#!/bin/bash

# Brahma Lite Setup Script
echo "🔧 Setting up Brahma Lite Chatbot..."

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | grep -oP '\d+\.\d+')
echo "Python version: $PYTHON_VERSION"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip -q

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Check .env file
if [ ! -f ".env" ]; then
    echo "⚠️ .env file not found"
    echo "Creating from .env.example..."
    cp .env.example .env
    echo "❗ Please edit .env and add your GOOGLE_API_KEY"
fi

# Check data files
if [ ! -f "data/events.json" ]; then
    echo "⚠️ data/events.json not found"
    echo "Please copy events.json to data/ directory"
else
    echo "✅ events.json found"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env and add your GOOGLE_API_KEY (if not already done)"
echo "2. Run: ./start.sh"
echo ""
echo "For manual start:"
echo "  source venv/bin/activate"
echo "  uvicorn app.main:app --host 0.0.0.0 --port 8000"
