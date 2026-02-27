#!/bin/bash

# Brahma Lite Chatbot Startup Script
# Optimized for 1-2GB RAM systems

echo "🚀 Starting Brahma Lite Chatbot..."

# Set memory limits (softer approach)
export OMP_NUM_THREADS=2
export PYTHONUNBUFFERED=1

# Don't use hard ulimit - can cause core dumps
# ulimit -v 2097152 2>/dev/null

# Check if running in low memory mode
AVAILABLE_MEM=$(free -m | awk 'NR==2{print $7}')
if [ "$AVAILABLE_MEM" -lt 1500 ]; then
    echo "⚠️  Low memory detected: ${AVAILABLE_MEM}MB available"
    echo "⚡ Using minimal settings..."
    export WORKERS=1
else
    echo "✅ Memory: ${AVAILABLE_MEM}MB available"
    export WORKERS=1
fi

# Start uvicorn with memory-efficient settings
uvicorn app.main:app \
    --host 0.0.0.0 \
    --port 4002 \
    --workers ${WORKERS} \
    --limit-concurrency 10 \
    --timeout-keep-alive 10 \
    --log-level info

# Cleanup on exit
trap 'echo "🧹 Cleaning up..."; pkill -f uvicorn' EXIT
