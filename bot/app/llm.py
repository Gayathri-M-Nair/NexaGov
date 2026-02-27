import os
import requests
from dotenv import load_dotenv

# Load .env BEFORE reading variables
load_dotenv()

# LLM API configuration - supports OpenAI, Groq, or any OpenAI-compatible API
LLM_API_URL = os.getenv("LLM_API_URL", "https://api.groq.com/openai/v1/chat/completions")
LLM_MODEL = os.getenv("LLM_MODEL", "llama-3.1-8b-instant")
LLM_API_KEY = os.getenv("LLM_API_KEY", "")

def generate_answer(context: str, question: str) -> str:
    """
    Generate answer using cloud LLM API (OpenAI-compatible format).
    Supports OpenAI, Groq, and other compatible APIs.
    """
    # Truncate context aggressively for faster processing
    max_context_length = 1000
    if len(context) > max_context_length:
        context = context[:max_context_length] + "..."
    
    # System prompt
    system_prompt = """You are a helpful assistant for Kerala Government Welfare Schemes.

🎯 YOUR JOB:
Answer questions about Kerala government schemes, benefits, eligibility, and application processes using ONLY the information provided in the context.

✅ WHEN TO ANSWER:
- If the context contains information relevant to the question, provide a clear, direct answer
- Answer naturally and conversationally
- Help users understand eligibility criteria, benefits, and step-by-step application roadmaps
- Explain documents needed and where to apply

❌ WHEN NOT TO ANSWER:
- If the context does NOT contain the information needed to answer the question
- If you would need to use general knowledge or make assumptions
- If the question is about schemes from other states not mentioned in context

🚫 STRICT RULES:
1. Use ONLY information from the context provided
2. DO NOT mention schemes from other states unless in the context
3. DO NOT use phrases like "typically", "usually", "generally" when describing specific schemes
4. If context is insufficient, respond: "I don't have that specific information about this scheme"
5. If question is not about Kerala schemes, respond: "I can only help with Kerala Government welfare schemes"
6. When explaining application process, provide step-by-step roadmap if available in context
"""

    user_prompt = f"""Context (your ONLY information source):
{context}

Question: {question}

Answer (be natural and helpful if context has the info, otherwise say you don't have it):"""

    try:
        print("🔄 Sending request to LLM API...")
        print(f"Context length: {len(context)}, Question: {question}")
        
        if not LLM_API_KEY:
            return "API key not configured. Please set LLM_API_KEY in your .env file."
        
        # Prepare request payload (OpenAI-compatible format)
        payload = {
            "model": LLM_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.05,
            "max_tokens": 150,
            "top_p": 0.7
        }
        
        # Prepare headers
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {LLM_API_KEY}"
        }
        
        # Make API request
        response = requests.post(
            LLM_API_URL,
            json=payload,
            headers=headers,
            timeout=30
        )
        response.raise_for_status()
        
        # Extract answer from response
        result = response.json()
        answer = result['choices'][0]['message']['content'].strip()
        
        # Post-processing filter: Check if answer mentions other states' schemes
        forbidden_terms = ["tamil nadu", "karnataka", "maharashtra", "delhi", "central government"]
        answer_lower = answer.lower()
        
        # If answer mentions forbidden terms, replace with standard response
        if any(term in answer_lower for term in forbidden_terms):
            return "I can only help with Kerala Government welfare schemes."
        
        # Check for suspiciously generic responses that might be hallucinated
        generic_phrases = [
            "typically", "usually", "generally", "most festivals", "common events",
            "standard events", "popular activities", "traditional"
        ]
        if any(phrase in answer_lower for phrase in generic_phrases):
            return "I don't have that specific information in the provided context."
        
        return answer
        
    except Exception as e:
        print(f"❌ LLM API error: {e}")
        return "Sorry, I couldn't generate a response at this time. Please check your API configuration."
