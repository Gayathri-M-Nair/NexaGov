from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
# --- ADDED THIS IMPORT ---
from fastapi.middleware.cors import CORSMiddleware
# -------------------------
from app.chat_engine import chat
from app.json_store import load_events_from_json
from app.cache import load_event_cache
from app.vector_store import build_vector_store, cleanup_resources
import traceback
import gc
import os
import signal
import sys
from datetime import datetime
from collections import defaultdict
import time
import subprocess
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ⚡ LIGHTWEIGHT: Limit worker threads
os.environ['UVICORN_WORKERS'] = '1'
os.environ['OMP_NUM_THREADS'] = '2'

# Authentication configuration
SYNC_TOKEN = os.getenv("SYNC_TOKEN", "your-secret-sync-token-here")
security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    """Verify bearer token for protected endpoints"""
    if credentials.credentials != SYNC_TOKEN:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials.credentials

# Global analytics tracking
ANALYTICS = {
    "start_time": None,
    "total_requests": 0,
    "successful_requests": 0,
    "failed_requests": 0,
    "errors": [],
    "llm_calls": 0,
    "semantic_search_calls": 0,
    "event_matches": 0,
    "pattern_matches": defaultdict(int),
    "response_times": [],
    "peak_memory_mb": 0,
    "last_error": None,
    "last_request_time": None,
}

# Handle signals gracefully
def signal_handler(sig, frame):
    print("\n⚠️ Received shutdown signal")
    cleanup_resources()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

app = FastAPI(
    title="Brahma Lite Chatbot",
    description="Memory-efficient version (1-2GB RAM)",
    version="1.0-lite"
)

# --- ADDED CORS CONFIGURATION HERE ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows your local HTML file to connect
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# -------------------------------------

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

class HealthResponse(BaseModel):
    status: str
    events_loaded: int


@app.on_event("startup")
def startup_event():
    """Initialize with memory constraints"""
    print("🚀 Starting Brahma Lite Chatbot...")
    print("⚡ Memory-efficient mode enabled")
    
    # Set start time for uptime tracking
    ANALYTICS["start_time"] = datetime.now()
    
    try:
        # Load events
        events = load_events_from_json()
        if not events:
            print("⚠️ No events loaded")
            return

        # Load into memory cache (limited)
        load_event_cache(events)

        # Build vector store (batch processing)
        build_vector_store(events)

        # Don't cleanup model immediately - keep it loaded
        # gc.collect()
        
        print(f"✅ Lite mode ready with {len(events)} events")
        print(f"💾 Memory footprint minimized")
        print("📡 Server ready to accept requests")
        
    except Exception as e:
        print(f"❌ Startup error: {e}")
        traceback.print_exc()
        # Don't crash the whole app
        import sys
        sys.exit(1)


@app.on_event("shutdown")
def shutdown_event():
    """Cleanup on shutdown"""
    print("🧹 Cleaning up resources...")
    cleanup_resources()
    gc.collect()


@app.get("/", response_model=HealthResponse)
def health_check():
    """Health check endpoint"""
    from app.cache import EVENT_CACHE
    return {
        "status": "healthy",
        "events_loaded": len(EVENT_CACHE)
    }


@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(req: ChatRequest):
    """Chat endpoint with error handling and analytics tracking"""
    start_time = time.time()
    
    try:
        # Update analytics
        ANALYTICS["total_requests"] += 1
        ANALYTICS["last_request_time"] = datetime.now().isoformat()
        
        # Truncate very long messages
        message = req.message[:500] if len(req.message) > 500 else req.message
        
        answer = chat(message)
        
        # Track successful request
        ANALYTICS["successful_requests"] += 1
        
        # Track response time
        response_time = time.time() - start_time
        ANALYTICS["response_times"].append(response_time)
        
        # Keep only last 100 response times for memory efficiency
        if len(ANALYTICS["response_times"]) > 100:
            ANALYTICS["response_times"] = ANALYTICS["response_times"][-100:]
        
        # Periodic garbage collection
        gc.collect()
        
        return {"reply": answer}

    except MemoryError:
        print("❌ MEMORY ERROR - System under pressure")
        ANALYTICS["failed_requests"] += 1
        ANALYTICS["last_error"] = {
            "type": "MemoryError",
            "time": datetime.now().isoformat(),
            "message": "System under memory pressure"
        }
        ANALYTICS["errors"].append(ANALYTICS["last_error"])
        
        # Keep only last 50 errors
        if len(ANALYTICS["errors"]) > 50:
            ANALYTICS["errors"] = ANALYTICS["errors"][-50:]
        
        gc.collect()
        return {
            "reply": "System is under memory pressure. Please try again."
        }
    
    except Exception as e:
        print(f"❌ CHAT ERROR: {e}")
        traceback.print_exc()
        
        ANALYTICS["failed_requests"] += 1
        ANALYTICS["last_error"] = {
            "type": type(e).__name__,
            "time": datetime.now().isoformat(),
            "message": str(e)
        }
        ANALYTICS["errors"].append(ANALYTICS["last_error"])
        
        # Keep only last 50 errors
        if len(ANALYTICS["errors"]) > 50:
            ANALYTICS["errors"] = ANALYTICS["errors"][-50:]
        
        return {
            "reply": "Sorry, something went wrong. Please try again."
        }


@app.get("/stats")
def stats(token: str = Depends(verify_token)):
    """
    Comprehensive analytics endpoint for monitoring and automation.
    Requires Bearer token authentication.
    
    Usage: curl http://localhost:8000/stats -H "Authorization: Bearer your-token"
    """
    from app.cache import EVENT_CACHE
    from app.vector_store import _collection
    import psutil
    
    # Calculate uptime
    uptime_seconds = 0
    uptime_formatted = "Not started"
    if ANALYTICS["start_time"]:
        uptime_delta = datetime.now() - ANALYTICS["start_time"]
        uptime_seconds = uptime_delta.total_seconds()
        days = uptime_delta.days
        hours, remainder = divmod(uptime_delta.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        uptime_formatted = f"{days}d {hours}h {minutes}m {seconds}s"
    
    # Calculate average response time
    avg_response_time = 0
    if ANALYTICS["response_times"]:
        avg_response_time = sum(ANALYTICS["response_times"]) / len(ANALYTICS["response_times"])
    
    # Get memory usage
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_mb = memory_info.rss / 1024 / 1024
    
    # Update peak memory if current is higher
    if memory_mb > ANALYTICS["peak_memory_mb"]:
        ANALYTICS["peak_memory_mb"] = memory_mb
    
    # Calculate success rate
    success_rate = 0
    if ANALYTICS["total_requests"] > 0:
        success_rate = (ANALYTICS["successful_requests"] / ANALYTICS["total_requests"]) * 100
    
    return {
        # System info
        "status": "healthy",
        "mode": "lightweight",
        "current_time": datetime.now().isoformat(),
        "uptime": {
            "seconds": uptime_seconds,
            "formatted": uptime_formatted,
            "start_time": ANALYTICS["start_time"].isoformat() if ANALYTICS["start_time"] else None
        },
        
        # Request metrics
        "requests": {
            "total": ANALYTICS["total_requests"],
            "successful": ANALYTICS["successful_requests"],
            "failed": ANALYTICS["failed_requests"],
            "success_rate_percent": round(success_rate, 2),
            "last_request_time": ANALYTICS["last_request_time"]
        },
        
        # Performance metrics
        "performance": {
            "average_response_time_ms": round(avg_response_time * 1000, 2),
            "total_responses_tracked": len(ANALYTICS["response_times"]),
            "current_memory_mb": round(memory_mb, 2),
            "peak_memory_mb": round(ANALYTICS["peak_memory_mb"], 2)
        },
        
        # Usage metrics
        "usage": {
            "llm_calls": ANALYTICS["llm_calls"],
            "semantic_search_calls": ANALYTICS["semantic_search_calls"],
            "event_matches": ANALYTICS["event_matches"],
            "pattern_matches": dict(ANALYTICS["pattern_matches"])
        },
        
        # Data metrics
        "data": {
            "cached_events": len(EVENT_CACHE),
            "vector_count": _collection.count() if _collection else 0
        },
        
        # Error tracking
        "errors": {
            "total_errors": ANALYTICS["failed_requests"],
            "recent_errors": ANALYTICS["errors"][-10:],  # Last 10 errors
            "last_error": ANALYTICS["last_error"]
        }
    }


@app.post("/sync")
def sync_events(token: str = Depends(verify_token)):
    """
    Sync events from Appwrite database.
    Requires Bearer token authentication.
    
    Usage: curl -X POST http://localhost:8000/sync -H "Authorization: Bearer your-token"
    """
    try:
        # Get the path to the sync script
        script_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "scripts", "sync_appwrite.py")
        
        if not os.path.exists(script_path):
            raise HTTPException(
                status_code=500,
                detail=f"Sync script not found at {script_path}"
            )
        
        # Run the sync script
        print("🔄 Starting event sync from Appwrite...")
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode != 0:
            print(f"❌ Sync failed: {result.stderr}")
            raise HTTPException(
                status_code=500,
                detail=f"Sync script failed: {result.stderr}"
            )
        
        print("✅ Sync completed successfully")
        
        # Reload events into cache and vector store
        try:
            events = load_events_from_json()
            load_event_cache(events)
            build_vector_store(events)
            
            return {
                "status": "success",
                "message": "Events synced successfully from Appwrite",
                "events_synced": len(events),
                "timestamp": datetime.now().isoformat(),
                "output": result.stdout
            }
        except Exception as reload_error:
            print(f"⚠️ Sync succeeded but reload failed: {reload_error}")
            return {
                "status": "partial_success",
                "message": "Events synced but cache reload failed. Restart server to apply changes.",
                "error": str(reload_error),
                "timestamp": datetime.now().isoformat(),
                "output": result.stdout
            }
    
    except subprocess.TimeoutExpired:
        raise HTTPException(
            status_code=504,
            detail="Sync operation timed out after 30 seconds"
        )
    
    except Exception as e:
        print(f"❌ Sync endpoint error: {e}")
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Sync failed: {str(e)}"
        )