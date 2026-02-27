import json
import re

def load_schemes():
    """Load schemes from JSON file"""
    try:
        with open("data/kerala_schemes.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("kerala_schemes", [])
    except Exception as e:
        print(f"Error loading schemes: {e}")
        return []

def search_schemes(query: str, schemes: list) -> str:
    """Simple keyword-based search in schemes"""
    query_lower = query.lower()
    
    # Check for greetings
    if any(word in query_lower for word in ["hi", "hello", "hey"]):
        return "Hello! I can help you find information about Kerala government schemes. Ask me about schemes for women, seniors, employment, housing, etc."
    
    # Check for thanks
    if any(word in query_lower for word in ["thank", "thanks"]):
        return "You're welcome! Feel free to ask if you need more information."
    
    # Search for matching schemes
    results = []
    for scheme in schemes:
        # Search in name, category, and benefit
        searchable_text = f"{scheme.get('name', '')} {scheme.get('category', '')} {scheme.get('benefit', '')}".lower()
        
        # Check if query words are in the scheme
        query_words = query_lower.split()
        matches = sum(1 for word in query_words if len(word) > 2 and word in searchable_text)
        
        if matches > 0:
            results.append((matches, scheme))
    
    # Sort by number of matches
    results.sort(reverse=True, key=lambda x: x[0])
    
    if not results:
        return "I couldn't find any schemes matching your query. Try asking about women welfare, senior citizens, employment, or housing schemes."
    
    # Return top result
    scheme = results[0][1]
    
    response = f"**{scheme['name']}**\n\n"
    response += f"Category: {scheme['category']}\n"
    response += f"Benefit: {scheme['benefit']}\n\n"
    
    # Add eligibility
    if 'eligibility' in scheme:
        response += "**Eligibility:**\n"
        for key, value in scheme['eligibility'].items():
            response += f"- {key.replace('_', ' ').title()}: {value}\n"
        response += "\n"
    
    # Add application steps
    if 'roadmap' in scheme and scheme['roadmap']:
        response += "**How to Apply:**\n"
        for step in scheme['roadmap'][:3]:  # Show first 3 steps
            response += f"{step['step']}. {step['title']}: {step['action']}\n"
    
    return response

def simple_chat(message: str) -> str:
    """Simple chat without AI - just keyword matching"""
    schemes = load_schemes()
    return search_schemes(message, schemes)
