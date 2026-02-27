#!/bin/bash

# Simplified Brahma Lite Startup (No aggressive limits)
echo "🚀 Starting Brahma Lite Chatbot (Safe Mode)..."

# Basic environment
export OMP_NUM_THREADS=2
export PYTHONUNBUFFERED=1

# Check memory
AVAILABLE_MEM=$(free -m | awk 'NR==2{print $7}')
echo "💾 Available memory: ${AVAILABLE_MEM}MB"

# Start with minimal settings (no trap that might interfere)
python3 -m uvicorn app.main:app \
    --host 0.0.0.0 \
    --port 4002 \
    --workers 1 \
    --log-level info

echo "Server stopped."
