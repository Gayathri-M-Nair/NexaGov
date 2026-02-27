# Brahma Lite Chatbot 🚀

A **lightweight, memory-efficient** version of the Brahma chatbot designed to run smoothly on systems with **1-2GB RAM** without crashing.

## ⚡ Key Optimizations

### Memory Efficiency
- **Smaller embedding model**: Uses `all-MiniLM-L6-v2` (22MB) instead of larger models
- **Limited batch processing**: Small batches (25 items) prevent memory spikes
- **Event cache limit**: Max 100 events cached in memory
- **Aggressive garbage collection**: Automatic cleanup after operations
- **Truncated context**: Limits text length to reduce memory footprint
- **Reduced vector search**: Returns 2 results instead of 3

### Crash Prevention
- **Memory error handling**: Gracefully handles out-of-memory situations
- **Resource cleanup**: Automatic cleanup on shutdown
- **Soft memory limits**: Uses ulimit to prevent hard crashes
- **Single worker mode**: Prevents worker process multiplication
- **Limited concurrency**: Max 10 concurrent requests

## 📋 Requirements

- Python 3.8+
- 1-2GB available RAM
- Ubuntu/Debian Linux (recommended)

## 🛠️ Installation

1. **Navigate to the lite directory:**
   ```bash
   cd brahma_lite
   ```

2. **Create virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Copy data files:**
   ```bash
   # Copy events.json from parent directory
   cp ../data/events.json data/
   
   # Copy fest document if available
   cp ../data/fest_info.docx data/ 2>/dev/null || echo "No fest_info.docx found (optional)"
   ```

5. **Set up environment variables:**
   ```bash
   # Copy .env from parent or create new
   cp ../.env . 2>/dev/null || echo "GOOGLE_API_KEY=your_api_key_here" > .env
   ```

## 🚀 Running

### Quick Start
```bash
chmod +x start.sh
./start.sh
```

### Manual Start
```bash
# Activate virtual environment
source venv/bin/activate

# Run with memory limits
export OMP_NUM_THREADS=2
uvicorn app.main:app --host 0.0.0.0 --port 4002 --workers 1
```

### Docker (Recommended for strict limits)
```bash
# Build with memory limit
docker build -t brahma-lite .

# Run with 1.5GB memory limit
docker run -p 4002:4002 --memory="1.5g" --memory-swap="1.5g" brahma-lite
```

## 📡 API Endpoints

### Health Check
```bash
curl http://localhost:4002/
```

### Chat
```bash
curl -X POST http://localhost:4002/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "When is the music event?"}'
```

### Stats
```bash
curl http://localhost:4002/stats
```

## 💾 Memory Footprint

| Component | Memory Usage |
|-----------|--------------|
| Base Python + FastAPI | ~150MB |
| Sentence Transformer Model | ~80MB |
| ChromaDB Vector Store | ~100MB |
| Event Cache (100 events) | ~10MB |
| Embeddings (100 docs) | ~50MB |
| **Total Typical Usage** | **~400-600MB** |
| **Peak Usage** | **~800MB-1GB** |

## 🔧 Configuration

Edit these values in the source files to tune memory usage:

### `app/cache.py`
```python
MAX_EVENTS = 100  # Reduce for less memory
```

### `app/vector_store.py`
```python
MAX_BATCH_SIZE = 25  # Smaller = less memory spikes
MAX_CACHE_SIZE = 100  # Limit vector store size
```

### `app/chat_engine.py`
```python
top_k=2  # Number of search results
```

## ⚠️ Troubleshooting

### Out of Memory Errors
```bash
# Check available memory
free -h

# Reduce limits in configuration files
# Restart with stricter limits
ulimit -v 1500000  # ~1.5GB limit
./start.sh
```

### Slow Performance
- Reduce `MAX_EVENTS` in cache.py
- Use fewer search results (`top_k=1`)
- Disable fest document loading

### Model Download Fails
```bash
# Pre-download the model
python3 -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')"
```

## 🆚 Differences from Full Version

| Feature | Full Version | Lite Version |
|---------|-------------|--------------|
| Embedding Model | all-MiniLM-L6-v2 (22MB) | Same but optimized |
| Events Cached | Unlimited | Max 100 |
| Batch Size | 50 | 25 |
| Search Results | 3 | 2 |
| Context Length | Full | Truncated (500 chars) |
| Memory Usage | 2-4GB | 400MB-1GB |

## 📝 Notes

- First startup is slower (downloads model ~22MB)
- Vector store is built once and persisted
- Automatic cleanup prevents memory leaks
- Suitable for edge devices, Raspberry Pi 4, or low-spec VPS

## 🔐 Security

- Set proper ulimits in production
- Use Docker memory limits for isolation
- Monitor memory usage with `/stats` endpoint

## 📄 License

Same as parent project

---

**Built for reliability on constrained hardware** ⚡
