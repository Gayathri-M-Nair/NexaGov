import chromadb
from chromadb.config import Settings
import os
import gc

# Force CPU mode and disable GPU
os.environ['CUDA_VISIBLE_DEVICES'] = ''
os.environ['OMP_NUM_THREADS'] = '2'  # Limit threading

from app.doc_loader import load_fest_documents

# ⚡ LIGHTWEIGHT: Use all-MiniLM-L6-v2 (22MB model, very efficient)
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
VECTOR_DIR = "vector_store_lite"
COLLECTION_NAME = "event_details_lite"
FEST_DOC_PATH = "data/festivals.txt"

# Memory limits
MAX_BATCH_SIZE = 25  # Smaller batches
MAX_CACHE_SIZE = 100  # Limit in-memory cache

_model = None
_collection = None
_client = None

def get_embedding_function():
    """Lazy load embedding model only when needed"""
    global _model
    
    if _model is None:
        print("🔧 Loading lightweight embedding model...")
        try:
            from sentence_transformers import SentenceTransformer
            # Use CPU and reduce threads to prevent crashes
            _model = SentenceTransformer(MODEL_NAME, device='cpu')
            # Reduce model memory footprint
            _model.max_seq_length = 128  # Shorter context
            print("✅ Model loaded successfully")
        except Exception as e:
            print(f"❌ Failed to load embedding model: {e}")
            raise
    
    return _model

def get_vector_components():
    global _collection, _client

    if _collection is None:
        print("🔧 Initializing lightweight ChromaDB...")
        # Use PersistentClient for actual persistence
        _client = chromadb.PersistentClient(
            path=VECTOR_DIR,
            settings=Settings(
                anonymized_telemetry=False,
                allow_reset=True
            )
        )
        _collection = _client.get_or_create_collection(
            name=COLLECTION_NAME
        )

    model = get_embedding_function()
    return model, _collection


def build_vector_store(events):
    """Build vector store with memory optimization"""
    model, collection = get_vector_components()

    # Skip if already built
    if collection.count() > 0:
        print("✅ Vector store already built. Skipping rebuild.")
        # Free model from memory after checking
        gc.collect()
        return

    documents = []
    metadatas = []
    ids = []

    # Limit number of events processed
    events_to_process = events[:MAX_CACHE_SIZE] if len(events) > MAX_CACHE_SIZE else events

    # Scheme documents - keep text concise
    for idx, scheme in enumerate(events_to_process):
        # Skip None/invalid schemes
        if scheme is None or not isinstance(scheme, dict):
            continue
        
        # Skip schemes without required fields
        if 'name' not in scheme:
            print(f"⚠️ Skipping scheme with missing name: {scheme}")
            continue
        
        # Use scheme id or generate one
        scheme_id = scheme.get('id', f"scheme_{idx}")
            
        # Build comprehensive text representation
        name = scheme.get('name', '')
        category = scheme.get('category', '')
        benefit = scheme.get('benefit', '')
        eligibility = str(scheme.get('eligibility', {}))
        roadmap = scheme.get('roadmap', [])
        
        # Create searchable text
        text = f"{name}. Category: {category}. Benefit: {benefit}. Eligibility: {eligibility}"
        if roadmap:
            text += f". Application has {len(roadmap)} steps."
        
        documents.append(text)
        metadatas.append({
            "type": "scheme",
            "scheme_id": scheme_id,
            "scheme_name": name
        })
        ids.append(scheme_id)

    # No additional documents needed - schemes are self-contained

    # Check if we have any documents to process
    if not documents:
        print("⚠️ No valid documents found to add to vector store")
        return

    # Process in small batches
    batch_size = MAX_BATCH_SIZE
    print(f"🔧 Encoding {len(documents)} documents (batches of {batch_size})...")
    
    for i in range(0, len(documents), batch_size):
        batch_end = min(i + batch_size, len(documents))
        batch_docs = documents[i:batch_end]
        batch_meta = metadatas[i:batch_end]
        batch_ids = ids[i:batch_end]
        
        # Encode with minimal memory footprint
        try:
            batch_embeddings = model.encode(
                batch_docs, 
                show_progress_bar=False,
                batch_size=8,  # Very small batch
                convert_to_numpy=True
            ).tolist()
            
            collection.upsert(
                documents=batch_docs,
                embeddings=batch_embeddings,
                metadatas=batch_meta,
                ids=batch_ids
            )
            
            # Clear memory after each batch
            del batch_embeddings
            gc.collect()
            
            print(f"  ✓ Batch {i//batch_size + 1}/{(len(documents)-1)//batch_size + 1}")
        except Exception as e:
            print(f"❌ Error processing batch {i//batch_size + 1}: {e}")
            continue

    print(f"✅ Lightweight vector store built with {len(documents)} documents.")
    
    # Gentle cleanup (don't force aggressive collection)
    # gc.collect()


def cleanup_resources():
    """Free up memory by clearing cached model"""
    global _model
    if _model is not None:
        del _model
        _model = None
        gc.collect()
        print("🧹 Cleaned up embedding model from memory")