# 🚀 Quick Start Guide - Brahma Lite

## Prerequisites
- Python 3.8+ installed
- 1-2GB available RAM
- Internet connection (first run only, for model download)

## 30-Second Setup

```bash
# Navigate to lite directory
cd brahma_lite

# Run setup (creates venv, installs packages)
./setup.sh

# Start the server
./start.sh
```

That's it! The server will be running at `http://localhost:4002`

## Test It

### In browser:
```
http://localhost:4002/
```

### Using curl:
```bash
# Health check
curl http://localhost:4002/

# Ask a question
curl -X POST http://localhost:4002/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Tell me about Brahma festival"}'

# Check stats
curl http://localhost:4002/stats
```

## Configuration

Edit `.env` if you need to update your API key:
```bash
GOOGLE_API_KEY=your_actual_api_key_here
```

## Memory Monitoring

Check memory usage while running:
```bash
# In another terminal
watch -n 2 'free -h && echo "" && ps aux | grep uvicorn | head -1'
```

## Troubleshooting

### "Out of Memory"
- Reduce `MAX_EVENTS` in `app/cache.py` (line 3)
- Reduce `MAX_CACHE_SIZE` in `app/vector_store.py` (line 13)
- Restart the server

### "Port already in use"
```bash
# Find and kill process on port 4002
lsof -ti:4002 | xargs kill -9
./start.sh
```

### "Model download fails"
```bash
# Pre-download model
source venv/bin/activate
python3 -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')"
```

## Docker Option

For even better isolation and memory control:

```bash
# Build
docker build -t brahma-lite .

# Run with 1.5GB memory limit
docker run -p 8000:8000 --memory="1.5g" --memory-swap="1.5g" \
  --env-file .env brahma-lite
```

## What's Different from Full Version?

- ✅ Uses **50% less memory** (400MB-1GB vs 2-4GB)
- ✅ **Won't crash** your system
- ✅ **Faster startup**
- ✅ Automatic memory cleanup
- ⚠️ Slightly slower responses (~100ms)
- ⚠️ Caches max 100 events instead of unlimited

See [COMPARISON.md](COMPARISON.md) for full details.

## Advanced Options

### Custom Port
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8080
```

### Production Mode
```bash
# With gunicorn for better process management
pip install gunicorn
gunicorn app.main:app -w 1 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Background Mode
```bash
nohup ./start.sh > output.log 2>&1 &
```

---

**Need help?** Check [README.md](README.md) for detailed documentation.
