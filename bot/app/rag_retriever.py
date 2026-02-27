from app.vector_store import get_vector_components
import gc

def semantic_search(query: str, top_k: int = 2):  # Conservative for system resources
    """Lightweight semantic search with minimal memory usage"""
    try:
        model, collection = get_vector_components()

        # Truncate long queries to save processing
        if len(query) > 200:
            query = query[:200]

        results = collection.query(
            query_texts=[query],
            n_results=top_k
        )

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]

        hits = []
        for doc, meta in zip(documents, metadatas):
            hits.append({
                "text": doc,
                "metadata": meta
            })

        # Debug output with type info
        if not hits:
            print("⚠️ No results")
        else:
            types = [h["metadata"].get("type", "unknown") for h in hits]
            type_counts = {}
            for t in types:
                type_counts[t] = type_counts.get(t, 0) + 1
            print(f"✓ Retrieved {len(hits)} docs: {type_counts}")

        # Clean up
        gc.collect()
        
        return hits
        
    except Exception as e:
        print(f"❌ Search error: {e}")
        return []