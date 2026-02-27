#!/usr/bin/env python3
"""
Alternative startup method - runs without uvicorn wrapper
Useful for debugging crashes
"""

import os
os.environ['OMP_NUM_THREADS'] = '2'
os.environ['PYTHONUNBUFFERED'] = '1'

print("🔧 Starting in debug mode...")

try:
    from app.main import app
    import uvicorn
    
    print("✅ Imports successful")
    print("🚀 Starting server on port 4002...")
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=4002,
        log_level="info",
        workers=1,
        limit_concurrency=10
    )
    
except KeyboardInterrupt:
    print("\n⚠️ Shutting down...")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
