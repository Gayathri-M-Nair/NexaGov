from app.cache import EVENT_CACHE
from app.rag_retriever import semantic_search
from app.llm import generate_answer
import re
import random

# Import analytics from main (will be set at runtime)
def get_analytics():
    """Get analytics dict from main module if available"""
    try:
        from app import main
        return main.ANALYTICS
    except (ImportError, AttributeError):
        return None

# ---------------- CONFIG ---------------- #

GREETING_RESPONSES = [
    "Hello! 👋 I'm here to help you with Kerala Government welfare schemes. Ask me about eligibility, benefits, or how to apply!",
    "Hi there! 😊 I can help you find information about Kerala schemes, benefits, and application processes. What would you like to know?",
    "Hey! 🎉 Welcome! I can assist you with Kerala Government schemes - eligibility, benefits, and step-by-step application guides.",
    "Greetings! I'm here to help with Kerala welfare schemes. Ask me about any scheme, eligibility criteria, or how to apply!",
]

THANKYOU_RESPONSES = [
    "You're welcome! Feel free to ask if you need anything else about Kerala schemes! 😊",
    "Happy to help! Let me know if you have more questions! 🎉",
    "Glad I could help! Ask away if you need more information!",
    "Anytime! Hope the information helps you! 🎊",
]

BYE_RESPONSES = [
    "Goodbye! 👋 Feel free to come back if you have more questions about Kerala schemes.",
    "See you later! 😊 I'm here whenever you need information about welfare schemes.",
    "Bye! Have a great day! 🎉",
    "Take care! 🌟 Reach out anytime for scheme information.",
]

OUT_OF_CONTEXT_RESPONSES = [
    "I can only help with Kerala Government welfare schemes.",
    "That's not related to Kerala schemes. Please ask about government welfare programs!",
    "I specialize in Kerala welfare schemes. Please ask about scheme eligibility, benefits, or applications!",
]

# ---------------- HELPERS ---------------- #

def is_greeting(query: str) -> bool:
    q_lower = query.lower().strip()
    q_norm = re.sub(r"(.)\1{2,}", r"\1\1", q_lower)
    greeting_words = {"hi", "hello", "hey", "hai", "hii", "heyy", "hola", "greetings", "yo"}
    words = re.findall(r"\b[a-zA-Z]+\b", q_norm)
    return any(w in greeting_words for w in words)

def is_thankyou(query: str) -> bool:
    q_lower = query.lower().strip()
    thanks_phrases = ["thanks", "thank you", "thankyou", "appreciate", "ty", "thx"]
    return any(phrase in q_lower for phrase in thanks_phrases)

def is_bye(query: str) -> bool:
    q_lower = query.lower().strip()
    bye_phrases = ["bye", "goodbye", "good bye", "see you", "see ya", "later", "cya"]
    return any(phrase in q_lower for phrase in bye_phrases)

def is_relevant_query(query: str) -> bool:
    """Check if query is about Kerala schemes"""
    keywords = ["scheme", "pension", "welfare", "benefit", "eligibility", "apply", 
                "application", "kerala", "sthree", "housing", "employment", "social security",
                "how to", "what is", "tell me", "register", "enroll"]
    q_lower = query.lower()
    return any(kw in q_lower for kw in keywords)

# ---------------- MAIN CHAT ---------------- #

def chat(user_message: str) -> str:
    """
    Chat function for Kerala schemes assistant
    """
    analytics = get_analytics()
    
    try:
        query = user_message.strip()
        if not query:
            return "Please ask a question."

        # 1. Handle pleasantries
        if is_greeting(query):
            if analytics:
                analytics["pattern_matches"]["greeting"] += 1
            return random.choice(GREETING_RESPONSES)
        
        if is_thankyou(query):
            if analytics:
                analytics["pattern_matches"]["thankyou"] += 1
            return random.choice(THANKYOU_RESPONSES)
        
        if is_bye(query):
            if analytics:
                analytics["pattern_matches"]["bye"] += 1
            return random.choice(BYE_RESPONSES)

        # 2. Check relevance
        if not is_relevant_query(query):
            if analytics:
                analytics["pattern_matches"]["out_of_context"] += 1
            return random.choice(OUT_OF_CONTEXT_RESPONSES)

        # 3. Use semantic search + LLM for all scheme queries
        if analytics:
            analytics["semantic_search_calls"] += 1
        
        docs = semantic_search(query, top_k=3)
        
        if not docs:
            return "I don't have information about that specific scheme. Please try asking about Sthree Suraksha, Social Security Pension, Employment schemes, or Housing schemes."
        
        # Build context from retrieved documents
        context_parts = []
        for doc in docs:
            # Get the text from the document
            text = doc.get("text", "")
            metadata = doc.get("metadata", {})
            
            # For schemes, we need to get the full data from cache
            scheme_id = metadata.get("scheme_id")
            if scheme_id:
                # Get full scheme data from cache
                from app.cache import EVENT_CACHE
                scheme = next((s for s in EVENT_CACHE if s.get('id') == scheme_id), None)
                
                if scheme:
                    name = scheme.get('name', 'Unknown Scheme')
                    category = scheme.get('category', '')
                    benefit = scheme.get('benefit', '')
                    eligibility = scheme.get('eligibility', {})
                    roadmap = scheme.get('roadmap', [])
                    
                    context_part = f"Scheme: {name}\n"
                    if category:
                        context_part += f"Category: {category}\n"
                    if benefit:
                        context_part += f"Benefit: {benefit}\n"
                    if eligibility:
                        context_part += f"Eligibility: {str(eligibility)}\n"
                    if roadmap:
                        context_part += f"Application Steps: {len(roadmap)} steps\n"
                        for step in roadmap[:3]:  # First 3 steps
                            context_part += f"  Step {step.get('step')}: {step.get('title')} - {step.get('action')}\n"
                    
                    context_parts.append(context_part)
                else:
                    # Fallback to just the text
                    context_parts.append(text)
            else:
                # Fallback to just the text
                context_parts.append(text)
        
        context = "\n\n".join(context_parts)
        
        # Generate answer using LLM
        if analytics:
            analytics["llm_calls"] += 1
        
        answer = generate_answer(context, query)
        return answer
        
    except Exception as e:
        print(f"❌ Chat error: {e}")
        import traceback
        traceback.print_exc()
        return "Sorry, something went wrong. Please try again."
