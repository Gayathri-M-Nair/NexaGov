import os
from dotenv import load_dotenv
from google import genai

# Load .env BEFORE reading variables
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise RuntimeError("❌ GOOGLE_API_KEY not found in environment")

client = genai.Client(api_key=API_KEY)
# ⚡ OPTIMIZED FOR SPEED: Using smallest Gemma model for fastest response
model = "models/gemma-3-1b-it"  # Fastest model with good quality

def generate_answer(context: str, question: str) -> str:
    """
    Generate answer with minimal token usage, optimized for speed.
    Ultra-strict prompt to prevent ANY hallucination.
    """
    # Truncate context aggressively for faster processing
    max_context_length = 1000  # Reduced from 1500
    if len(context) > max_context_length:
        context = context[:max_context_length] + "..."
    
    # ULTRA-STRICT prompt to prevent hallucination
    prompt = f"""You are a helpful assistant for Brahma '26 and Ashwamedha '26 festivals at ASIET.

🎯 YOUR JOB:
Answer questions about Brahma '26 and Ashwamedha '26 using ONLY the information provided in the context below.

✅ WHEN TO ANSWER:
- If the context contains information relevant to the question, provide a clear, direct answer
- Answer naturally and conversationally
- You can answer questions in any format: "history of brahma", "what is brahma history", "tell me brahma history", etc.

❌ WHEN NOT TO ANSWER:
- If the context does NOT contain the information needed to answer the question
- If you would need to use general knowledge or make assumptions
- If the question is about other colleges/festivals not mentioned in context

🚫 STRICT RULES:
1. Use ONLY information from the context provided
2. DO NOT mention other colleges/festivals (IIT, NIT, CUSAT, Prayag, Tathva, etc.)
3. DO NOT use phrases like "typically", "usually", "generally", "most festivals"
4. If context is insufficient, respond: "I don't have that specific information"
5. If question is not about Brahma '26 or Ashwamedha '26, respond: "I can only help with Brahma '26 and Ashwamedha '26 events at ASIET"

Context (your ONLY information source):
{context}

Question: {question}

Answer (be natural and helpful if context has the info, otherwise say you don't have it):"""

    try:
        print("🔄 Sending request to LLM...")
        print(f"Context length: {len(context)}, Question: {question}")
        
        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config={
                'max_output_tokens': 150,  # Reduced for faster response
                'temperature': 0.05,  # ULTRA-LOW temperature to minimize creativity
                'top_p': 0.7,  # Further reduce randomness
                'top_k': 10,  # Stricter token selection
            }
        )
        
        answer = response.text.strip()
        
        # Post-processing filter: Check if answer mentions other fests/colleges
        forbidden_terms = ["prayag", "tathva", "dhwani", "iit ", "nit ", "cusat", "mec ", "rajagiri", 
                          "iit-", "nit-", "mec-"]
        answer_lower = answer.lower()
        
        # If answer mentions forbidden terms, replace with standard response
        if any(term in answer_lower for term in forbidden_terms):
            return "I can only help with Brahma '26 and Ashwamedha '26 events at ASIET."
        
        # Check for suspiciously generic responses that might be hallucinated
        generic_phrases = [
            "typically", "usually", "generally", "most festivals", "common events",
            "standard events", "popular activities", "traditional"
        ]
        if any(phrase in answer_lower for phrase in generic_phrases):
            return "I don't have that specific information in the provided context."
        
        return answer
        
    except Exception as e:
        print(f"❌ LLM error: {e}")
        return "Sorry, I couldn't generate a response at this time."