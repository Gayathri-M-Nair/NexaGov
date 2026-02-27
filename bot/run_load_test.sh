#!/bin/bash

# Load Testing Script for Brahma Lite
# Tests if the system crashes under load

echo "🧪 Brahma Lite Load Test"
echo "========================"
echo ""

# Check if locust is installed
if ! command -v locust &> /dev/null; then
    echo "❌ Locust not found. Installing..."
    pip install locust
fi

# Check if server is running
if ! curl -s http://localhost:4002/ > /dev/null 2>&1; then
    echo "❌ Server not running on port 4002"
    echo "   Start it with: ./start_safe.sh"
    exit 1
fi

echo "✅ Server is running"
echo ""

# Run different test scenarios
echo "Choose a test scenario:"
echo "1. Light test (10 users, 2/sec spawn)"
echo "2. Medium test (50 users, 5/sec spawn)"
echo "3. Heavy test (100 users, 10/sec spawn)"
echo "4. Stress test (200 users, 20/sec spawn)"
echo "5. Custom"
echo ""
read -p "Enter choice [1-5]: " choice

case $choice in
    1)
        USERS=10
        SPAWN_RATE=2
        RUN_TIME="2m"
        ;;
    2)
        USERS=50
        SPAWN_RATE=5
        RUN_TIME="3m"
        ;;
    3)
        USERS=100
        SPAWN_RATE=10
        RUN_TIME="5m"
        ;;
    4)
        USERS=200
        SPAWN_RATE=20
        RUN_TIME="5m"
        ;;
    5)
        read -p "Number of users: " USERS
        read -p "Spawn rate (users/sec): " SPAWN_RATE
        read -p "Run time (e.g. 2m, 30s): " RUN_TIME
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac

echo ""
echo "🚀 Starting load test:"
echo "   Users: $USERS"
echo "   Spawn rate: $SPAWN_RATE/sec"
echo "   Duration: $RUN_TIME"
echo ""
echo "📊 Monitor:"
echo "   Web UI: http://localhost:8089"
echo "   Server: http://localhost:4002/stats"
echo ""
echo "Press Ctrl+C to stop early"
echo ""

# Run locust
locust -f locustfile.py \
    --host=http://localhost:4002 \
    --users=$USERS \
    --spawn-rate=$SPAWN_RATE \
    --run-time=$RUN_TIME \
    --headless \
    --html=load_test_report.html \
    --csv=load_test_results

echo ""
echo "✅ Test complete!"
echo ""
echo "📊 Results saved:"
echo "   HTML Report: load_test_report.html"
echo "   CSV Data: load_test_results_*.csv"
echo ""

# Check server status
echo "🔍 Checking server status..."
if curl -s http://localhost:4002/ > /dev/null 2>&1; then
    echo "✅ Server still running - No crash!"
    curl -s http://localhost:4002/stats | python3 -m json.tool
else
    echo "❌ Server crashed or stopped"
fi
