#!/usr/bin/env python3
"""
Quick validation script for Brahma Lite
Tests imports and basic functionality without starting server
"""

import sys
import os

print("🔍 Validating Brahma Lite setup...")
print()

# Test 1: Python version
print("1. Python version check...")
if sys.version_info >= (3, 8):
    print(f"   ✅ Python {sys.version_info.major}.{sys.version_info.minor}")
else:
    print(f"   ❌ Python {sys.version_info.major}.{sys.version_info.minor} (need 3.8+)")
    sys.exit(1)

# Test 2: Required files
print("\n2. Required files check...")
required_files = [
    "app/main.py",
    "app/vector_store.py", 
    "app/chat_engine.py",
    "requirements.txt",
    "data/events.json"
]

all_exist = True
for f in required_files:
    if os.path.exists(f):
        print(f"   ✅ {f}")
    else:
        print(f"   ❌ {f} missing")
        all_exist = False

if not all_exist:
    sys.exit(1)

# Test 3: Dependencies
print("\n3. Dependencies check...")
try:
    import fastapi
    print("   ✅ fastapi")
except ImportError:
    print("   ❌ fastapi not installed")
    print("   → Run: ./setup.sh")
    sys.exit(1)

try:
    import chromadb
    print("   ✅ chromadb")
except ImportError:
    print("   ❌ chromadb not installed")
    sys.exit(1)

try:
    from sentence_transformers import SentenceTransformer
    print("   ✅ sentence-transformers")
except ImportError:
    print("   ❌ sentence-transformers not installed")
    sys.exit(1)

try:
    from google import genai
    print("   ✅ google-genai")
except ImportError:
    print("   ❌ google-genai not installed")
    sys.exit(1)

# Test 4: Environment
print("\n4. Environment check...")
if os.path.exists(".env"):
    print("   ✅ .env file exists")
    with open(".env") as f:
        content = f.read()
        if "GOOGLE_API_KEY" in content and "your_" not in content.lower():
            print("   ✅ GOOGLE_API_KEY configured")
        else:
            print("   ⚠️  GOOGLE_API_KEY not configured")
            print("   → Edit .env and add your API key")
else:
    print("   ⚠️  .env file not found")
    print("   → Copy .env.example to .env and configure")

# Test 5: Data
print("\n5. Data check...")
try:
    import json
    with open("data/events.json") as f:
        data = json.load(f)
        events = data.get("events", [])
        print(f"   ✅ {len(events)} events loaded")
except Exception as e:
    print(f"   ❌ Error loading events: {e}")

# Test 6: Memory requirements
print("\n6. System resources...")
try:
    import psutil
    mem = psutil.virtual_memory()
    available_gb = mem.available / (1024**3)
    print(f"   ℹ️  Available RAM: {available_gb:.1f}GB")
    if available_gb >= 1.5:
        print("   ✅ Sufficient memory")
    else:
        print("   ⚠️  Low memory - may need to reduce limits")
except ImportError:
    print("   ℹ️  Install psutil to check memory")

print("\n" + "="*60)
print("✅ Validation complete!")
print()
print("Ready to start:")
print("   ./start.sh")
print()
print("Or manually:")
print("   source venv/bin/activate")
print("   uvicorn app.main:app --host 0.0.0.0 --port 8000")
print("="*60)
