from app.cache import EVENT_CACHE, get_event_by_name
from app.rag_retriever import semantic_search
from app.llm import generate_answer
import re
import random
from difflib import SequenceMatcher
import gc

# Import analytics from main (will be set at runtime)
def get_analytics():
    """Get analytics dict from main module if available"""
    try:
        from app import main
        return main.ANALYTICS
    except (ImportError, AttributeError):
        return None

# ---------------- CONFIG ---------------- #

# Response variations
BRAHMA_RESPONSES = [
    "Brahma '26 is the annual cultural festival of Adi Shankara Institute of Engineering and Technology (ASIET), celebrating music, dance, art, and creative expression.",
    
    "Brahma is ASIET's flagship cultural fest featuring competitive events, pro-shows, and workshops that showcase student talent.",
    
    "Brahma '26 is ASIET's premier cultural festival where students shine through music, dance, drama, and various art forms.",
    
    "The Brahma festival is ASIET's biggest cultural celebration with exciting events, competitions, and unforgettable performances.",
    
    "Brahma '26 brings together students for an amazing cultural experience at ASIET with diverse events and activities.",
    
    "Brahma is ASIET's grand cultural extravaganza showcasing creativity, talent, and student spirit through vibrant performances.",
    
    "Brahma '26 is where culture meets creativity at ASIET! Expect dance battles, music competitions, and exciting stage events.",
    
    "ASIET's Brahma '26 is the ultimate cultural fest featuring everything from traditional performances to modern artistic expressions.",
    
    "Brahma '26 celebrates the artistic spirit of ASIET with engaging competitions, workshops, and spectacular shows.",
    
    "It's ASIET's biggest cultural celebration! Brahma '26 offers students a platform to perform, compete, and connect through art and culture."
]


ASHWAMEDHA_RESPONSES = [
    "Ashwamedha is ASIET's national-level technical fest showcasing innovation and engineering excellence.",
    
    "Ashwamedha features coding contests, hackathons, robotics events, and technical competitions for tech enthusiasts.",
    
    "Ashwamedha is the technical fest at ASIET where students showcase their engineering skills and innovative ideas.",
    
    "ASIET's Ashwamedha is a premier technical festival with competitions in coding, robotics, and various tech domains.",
    
    "Ashwamedha brings together tech enthusiasts for exciting technical competitions and workshops at ASIET.",
    
    "Ashwamedha is ASIET's biggest tech fest featuring hackathons, robotics challenges, and cutting-edge technical events.",
    
    "It's all about innovation! Ashwamedha is ASIET's national-level technical festival with coding, robotics, and engineering competitions.",
    
    "Ashwamedha celebrates technical excellence at ASIET through challenging events, hands-on workshops, and competitive programming.",
    
    "ASIET's Ashwamedha offers students a platform to compete, innovate, and showcase their technical prowess.",
    
    "Ashwamedha is where engineering meets innovation! Join ASIET's premier technical fest for exciting challenges and competitions."
]


OUT_OF_CONTEXT_RESPONSES = [
    "I can help only with Brahma '26 and Ashwamedha'26 events.",
    "That's not related to the Brahma festival.",
    "I specialize in Brahma '26 and Ashwamedha information. Please ask about festival events!",
    "Sorry, I can only assist with questions about Brahma '26 and ASIET events.",
    "That's outside my scope. I'm here to help with Brahma and Ashwamedha related queries!"
]

GREETING_RESPONSES = [
    "Hello! 👋 I'm the Brahma ’26 & Ashwamedha ’26 assistant. Ask me about events, dates, venues, or anything related to ASIET fests!",
    "Hi there! 😊 I can help you with information about Brahma ’26 cultural events and Ashwamedha ’26 technical events at ASIET. What would you like to know?",
    "Hey! 🎉 Welcome to the Brahma ’26 & Ashwamedha ’26 info bot. Ask me about cultural or technical events, schedules, and venues!",
    "Greetings! I'm here to help with both Brahma ’26 and Ashwamedha ’26 events at ASIET. What can I tell you about?",
    "Hello! 🌟 Looking for details on Brahma ’26 or Ashwamedha ’26? I’ve got you covered with event info, timings, and venues!",
    "Hi! 👋 This is the official assistant for ASIET’s Brahma ’26 and Ashwamedha ’26 fests. Feel free to ask about any event!",
    "Hey there! 🎊 Whether it’s Brahma ’26 or Ashwamedha ’26, I can help you with event details, registration info, and schedules.",
    "Welcome! 😊 Ask me anything about ASIET’s Brahma ’26 cultural fest or Ashwamedha ’26 technical fest — I’m here to help!",
]


THANKYOU_RESPONSES = [
    "You're welcome! Feel free to ask if you need anything else about Brahma '26! 😊",
    "Happy to help! Let me know if you have more questions about the fest! 🎉",
    "Glad I could help! Ask away if you need more info about ASIET events!",
    "Anytime! Enjoy Brahma '26! 🎊",
]
OKAY_RESPONSES = [
    "Perfect! Let me know if you need anything else. 😊",
    "Got it! I'm here if you have more questions about Brahma and Ashwamedha. ⚙️",
    "Great! What else can I help you with today? 🚀",
    "Understood. Feel free to ask about events, venues, or schedules anytime!",
    "Happy to help! Just shout if you need more info on ASIET's tech fest. 🛠️"
]
BYE_RESPONSES = [
    "Goodbye! 👋 Feel free to come back if you have more questions about Brahma ’26 or Ashwamedha ’26.",
    "See you later! 😊 I’m here whenever you need information about ASIET events.",
    "Bye! Have a great day and enjoy the festivities at Brahma ’26 and Ashwamedha ’26.",
    "Take care! 🎉 Reach out anytime for details about cultural or technical events at ASIET.",
    "Goodbye! 🌟 Hope you have an amazing experience at Brahma ’26 and Ashwamedha ’26.",
    "See you soon! 👋 Don’t hesitate to ask if you need more event information.",
    "Bye for now! 😊 Wishing you a fun and memorable time at ASIET fests.",
    "Thanks for chatting! 🎊 Come back anytime to learn more about Brahma ’26 or Ashwamedha ’26.",
    "Goodbye! 👋 All the best, and enjoy exploring the events at ASIET.",
    "Catch you later! 🚀 I’ll be here to help whenever you need fest-related details."
]
ABUSE_RESPONSES = [
    "I’m here to help. Let’s keep the conversation respectful.",
    "I understand frustration, but I’m here to assist you with Brahma ’26 and Ashwamedha ’26.",
    "Let’s keep things polite. Ask me about events, schedules, or venues.",
    "I’m designed to help with festival-related queries. How can I assist you?",
    "No worries—if something didn’t work, try asking about an event or fest detail.",
    "I’m here to provide information, not to argue. What would you like to know?",
    "Let’s stay respectful. I can help with Brahma ’26 and Ashwamedha ’26 events.",
    "I’m focused on helping you with festival information. Ask away!",
    "If you’re looking for event details, I’m happy to help.",
    "Let’s get back to the fest! What would you like to know about Brahma or Ashwamedha?"
]
BRAHMA_REGISTRATION_RESPONSES = [
    "To register for Brahma '26:\n\n"
    "1. Visit the official Brahma '26 page: https://www.asietfest.in/brahma\n\n"
    "2. Each participant must register individually\n\n"
    "3. Create or join your team using the registered IDs\n\n"
    "4. Complete the payment process\n\n"
    "5. Event tickets will be sent to your registered email ID\n\n"
    "6. Please check your spam/junk folder as well\n\n"
    "For help, contact the respective event coordinators."
]

ASHWAMEDHA_REGISTRATION_RESPONSES = [
    "To register for Ashwamedha '26:\n\n"
    "1. Visit the official Ashwamedha '26 page: https://www.asietfest.in/ashwamedha\n\n"
    "2. Each participant must register individually\n\n"
    "3. Create or join your team using the registered IDs\n\n"
    "4. Complete the payment process\n\n"
    "5. Event tickets will be sent to your registered email ID\n\n"
    "6. Please check your spam/junk folder as well\n\n"
    "For help, contact the respective event coordinators."]
# ---------------- EVENT LIST RESPONSES ---------------- #

BRAHMA_GENERAL_EVENTS = [
    "Soap Soccer",
    "BGMI (Online)",
    "Shoutout Clash",
    "Carnival Nexus",
    "Clue Crusade",
    "Game of Rooms",
    "Challengers Arena",
    "Knives Out",
    "Paint Ball",
    "Spot Photography",
    "ASIET Talkies",
    "Retro Carroms",
    "FIFA Fever",
    "Product Pioneers",
    "Underarm Cricket",
    "Militia Madness",
    "R J Hunt",
    "Pitch in 120 Seconds",
    "Strike 3",
    "Sumo Wrestling",
    "IPL Auction",
    "Guess-O-Holic",
    "Gyro Glide",
    "Valorant (Online)",
    "E Football (Online)",
    "Glow Ball",
    "AFT Workshop"
]

BRAHMA_CULTURAL_EVENTS = [
    "Doodling",
    "Mime",
    "Band of Brahma",
    "Ragam",
    "Step N Syncro",
    "Spot Dance",
    "Mudhra",
    "Voice of Brahma",
    "DJ War",
    "Choreo Night",
    "Theme Show"
]

# Fake technical events for Brahma (temporary)
BRAHMA_TECHNICAL_EVENTS = [
    "Code Blitz",
    "Debug Dominion",
    "HackSprint",
    "Logic Lords",
    "Binary Battle",
    "Tech Quest"
]

ASHWAMEDHA_TECHNICAL_EVENTS = [
    "Capture the Flag – Cyber Security Hackathon",
    "Neuro Clash",
    "Prompt & Roast (AI Prompting)",
    "Eyes Off",
    "PlanScape",
    "Structostick",
    "Paradox Arena",
    "Stranger Games",
    "Synapse Spark (Ideathon)",
    "Code Red Clues (Escape Room)",
    "Robo Pixel – ML/AI",
    "Line Follower",
    "Circuit Bombing",
    "Electrothon",
    "Tech Trivia",
    "Remote Car Race",
    "VR Experience",
    "Technical Treasure Hunt",
    "TECH FUSION 25 (Workshop Series)",
    "Drone Show and Expo",
    "IoT Based Workshop",
    "Thinker Hub",
    "Workshop (FPGA)"
]



BYE_RESPONSES = [
    "Goodbye! See you at Brahma '26! 🎉",
    "Bye! Have a great time at the fest! 👋",
    "See you later! Don't miss Brahma '26! 🎊",
    "Take care! Enjoy the festival! 😊",
]

HELP_RESPONSES = [
    "I can help you with: Event details, dates, times, venues, coordinators, and festival information. Just ask!",
    "Ask me about Brahma '26 events, schedules, locations, or anything related to ASIET's cultural fest!",
    "I'm here to answer questions about event timings, venues, coordinators, and festival details. What would you like to know?",
]

IDENTITY_RESPONSES = [
    "I'm the Brahma '26 assistant bot! I help with information about ASIET's cultural festival. 🎭",
    "I'm your friendly Brahma '26 info bot, here to answer questions about the fest! 🎉",
    "I'm an AI assistant dedicated to helping you with Brahma '26 and ASIET event information! 😊",
]

CAPABILITY_RESPONSES = [
    "I can tell you about event schedules, venues, dates, coordinators, and details about Brahma '26 and Ashwamedha festivals!",
    "I provide information on all Brahma '26 events including timings, locations, and how to participate. Ask away!",
    "I help with event details, festival schedules, venue information, and coordinator contacts for Brahma '26! 🎊",
]

# ---------------- HELPERS ---------------- #

def tokenize(text: str) -> set:
    return set(re.findall(r"\b[a-zA-Z]+\b", text.lower()))
def is_abusive_query(query: str) -> bool:
    q = query.lower().strip()
    words = set(re.findall(r"\b[a-zA-Z]+\b", q))

    # Short words need whole-word matching to avoid false positives
    short_abusive = ["mad", "bad", "dumb"]
    if any(word in words for word in short_abusive):
        return True
    
    # Longer phrases can use substring matching
    abusive_phrases = [
        "stupid",
        "idiot",
        "useless",
        "crazy",
        "are you stupid",
        "are you dumb",
        "you are stupid",
        "you are dumb",
        "bad bot",
        "worst bot",
        "nonsense bot",
        "hello bitch",
        "hello stupid monkey bot",
        "shut up"
    ]

    return any(phrase in q for phrase in abusive_phrases)


def is_meta_question(query: str) -> bool:
    q = query.lower().strip()

    meta_phrases = [
        "who made you",
        "who created you",
        "who built you",
        "who developed you",
        "are you real",
        "are you human",
        "what are you",
        "who are you",
        "your creator",
        "your developer"
        "user details"
        "user table details"
        "give db information"
        "give access"
    ]

    # Phrase match
    for phrase in meta_phrases:
        if phrase in q:
            return True

    return False

def normalize_text(text: str) -> str:
    """Normalize text by removing spaces, hyphens, and converting to lowercase"""
    return re.sub(r"[\s-]+", "", text.lower())

def safe(val, fallback="not specified"):
    return val if val else fallback
def format_names(names):
    if not names or names == "not specified":
        return "not specified"
    if isinstance(names, list):
        if len(names) == 1:
            return names[0]
        if len(names) == 2:
            return f"{names[0]} and {names[1]}"
        return ", ".join(names[:-1]) + f" and {names[-1]}"
    return names

def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

FEST_ALIASES = {
    "brahma": ["brahma", "brama", "bhrahma", "brahama", "bramma", "bramha"],
    "ashwamedha": ["ashwamedha", "aswamedha", "ashwmedha", "ashwameda", "aswameda", "ashvameda"]
}

def fuzzy_fest_match(query: str, threshold: float = 0.70):
    """Check if any word in query matches fest names with fuzzy matching"""
    q_lower = query.lower()
    
    # Check each word in the query
    words = re.findall(r"\b[a-zA-Z]+\b", q_lower)
    
    for fest, variants in FEST_ALIASES.items():
        for v in variants:
            # Check if variant appears in query (exact substring)
            if v in q_lower:
                return fest
            
            # Check similarity of each word in query
            for word in words:
                # Use lower threshold for longer words (more room for typos)
                word_threshold = threshold if len(word) < 8 else 0.65
                if len(word) >= 4 and similarity(word, v) >= word_threshold:
                    return fest
    
    return None

def find_exact_event(query: str):
    """Find event with simplified matching, handles typos"""
    q_tokens = tokenize(query)
    q_lower = query.lower().strip()
    matched = []

    # Search through all cached events
    for event in EVENT_CACHE:
        name = event.get("event_name", "")
        if not name:
            continue
            
        name_lower = name.lower().strip()
        e_tokens = tokenize(name)

        # 1. Exact substring match (highest priority)
        if name_lower in q_lower:
            matched.append(event)
            continue

        # 2. Token-based match (all event name words in query)
        if e_tokens and e_tokens.issubset(q_tokens):
            matched.append(event)
            continue
        
        # 3. Fuzzy token match (handles typos like "inifinity" -> "infinity")
        if e_tokens and len(e_tokens) >= 2:
            fuzzy_matches = 0
            for e_word in e_tokens:
                if len(e_word) < 4:  # Skip short words
                    continue
                for q_word in q_tokens:
                    if len(q_word) < 4:
                        continue
                    if similarity(e_word, q_word) > 0.85:
                        fuzzy_matches += 1
                        break
            # If most event words have fuzzy matches
            if fuzzy_matches >= len([w for w in e_tokens if len(w) >= 4]):
                matched.append(event)
                continue

    if len(matched) == 1:
        return matched[0]
    
    # If multiple matches, prefer exact substring
    if len(matched) > 1:
        for event in matched:
            name_lower = event.get("event_name", "").lower()
            if name_lower in q_lower:
                return event
        # Return first match
        return matched[0]
    
    return None

def is_greeting(query: str) -> bool:
    q_lower = query.lower().strip()

    # Normalize repeated letters: heyyyy → heyy
    q_norm = re.sub(r"(.)\1{2,}", r"\1\1", q_lower)

    greeting_words = {
        "hi", "hello", "hey", "hai", "hii", "heyy",
        "hola", "greetings", "yo", "help", "helpp"
    }

    filler_words = {
        "my", "dear", "bot", "there", "buddy",
        "friend", "bro", "man", "sir", "mam"
    }

    words = re.findall(r"\b[a-zA-Z]+\b", q_norm)

    # Remove fillers
    meaningful = [w for w in words if w not in filler_words]
    
    # For single-word queries, use exact match (prevents "helpful" from matching "help")
    if len(meaningful) == 1:
        if meaningful[0] in greeting_words:
            return True
        # Fuzzy match for typos
        for g in greeting_words:
            if len(meaningful[0]) >= 3 and similarity(meaningful[0], g) >= 0.75:
                return True
        return False

    # For multi-word queries, exact greeting match
    if any(w in greeting_words for w in meaningful):
        return True

    # Fuzzy greeting match (handles helo, hllo, helloo)
    for w in meaningful:
        for g in greeting_words:
            if len(w) >= 3 and similarity(w, g) >= 0.75:
                return True

    return False


def is_thankyou(query: str) -> bool:
    q_lower = query.lower().strip()

    # Normalize repeated letters: thanksss -> thankss
    q_norm = re.sub(r"(.)\1{2,}", r"\1\1", q_lower)

    # Extract words for whole-word matching
    words = set(re.findall(r"\b[a-zA-Z]+\b", q_norm))
    
    # Short thank-you words need exact word match (to avoid "infinity" matching "ty")
    short_thanks = ["ty", "thx"]
    if any(word in words for word in short_thanks):
        return True
    
    # Longer phrases can use substring match
    long_thanks = ["thanks", "thank you", "thankyou", "appreciate"]
    for phrase in long_thanks:
        if phrase in q_norm:
            return True

    # Fuzzy word-level match for spelling mistakes (only for longer words)
    for w in words:
        if len(w) >= 5:  # Only check words 5+ characters to avoid false matches
            for t in ["thanks", "thank"]:
                if similarity(w, t) >= 0.7:
                    return True

    return False

def is_bye(query: str) -> bool:
    q_lower = query.lower().strip()

    # Normalize repeated characters: byeee → byee → bye
    q_norm = re.sub(r"(.)\1{2,}", r"\1\1", q_lower)
    
    # Extract words for whole-word matching
    words = set(re.findall(r"\b[a-zA-Z]+\b", q_norm))

    # Short words that need exact word match (to avoid "no" matching "know", "innovation", etc.)
    short_byes = ["no", "bye", "tata", "later", "cya", "exit", "quit", "close"]
    if any(word in words for word in short_byes):
        return True
    
    # Longer phrases can use substring matching
    bye_phrases = [
        "bye bye", "byebye", "goodbye", "good bye",
        "see you", "see ya",
        "ta ta",
        "sign off", "signoff"
    ]

    # Phrase match (for multi-word goodbyes)
    return any(phrase in q_norm for phrase in bye_phrases)



def is_okay(query: str) -> bool:
    """Check if message is a variation of 'ok' using flexible pattern matching"""
    q_lower = query.lower().strip()
    words = set(re.findall(r"\b[a-zA-Z]+\b", q_lower))
    
    # Short single-letter responses need to be standalone (to avoid matching 'k' in words)
    if q_lower in ["k", "kk", "kkk", "ok"]:
        return True
    
    # Longer ok variations can use pattern matching
    ok_pattern = r"^(okay|oke|oky|okie|hokay|okeoke|ogey|keke|okeokekk)[eyio]*$"
    
    # Also catch repetitive cases like "okeoke"
    if any(var in q_lower for var in ["okeoke", "ok ok"]):
        return True
        
    return bool(re.match(ok_pattern, q_lower))
def is_registration_query(query: str) -> bool:
    """Check if the query is about registration process"""
    q_lower = query.lower().strip()
    
    registration_keywords = [
        "how to register",
        "how do i register",
        "how can i register",
        "register for",
        "registration process",
        "registration steps",
        "how to participate",
        "how do i participate",
        "how to join",
        "how do i join",
        "how to enroll",
        "enrollment process",
        "sign up for",
        "how to sign up",
        "participate in event",
        "join the event",
        "registration procedure",
        "how register"
    ]
    
    return any(keyword in q_lower for keyword in registration_keywords)
def format_event_list(title: str, events: list[str]) -> str:
    """Format event list with proper header and bullet points"""
    event_lines = "\n".join(f"• {e}" for e in events)
    return f"Here's the event list for {title}:\n\n{event_lines}"


def is_goodbye(query: str) -> bool:
    """Check if message is a goodbye"""
    goodbyes = ["bye", "goodbye", "good bye", "see you", "see ya", "later", "farewell", "cya"]
    q_lower = query.lower().strip()
    return any(g in q_lower for g in goodbyes) and len(q_lower.split()) <= 3

def is_help_request(query: str) -> bool:
    """Check if user is asking for help"""
    help_keywords = ["help", "how to use", "what can you do", "how do you work", "guide", "assist"]
    q_lower = query.lower().strip()
    return any(h in q_lower for h in help_keywords) and len(q_lower.split()) <= 6

def is_identity_question(query: str) -> bool:
    """Check if user is asking who the bot is"""
    identity_patterns = ["who are you", "what are you", "your name", "who r u", "what r u"]
    q_lower = query.lower().strip()
    return any(p in q_lower for p in identity_patterns)

def is_capability_question(query: str) -> bool:
    """Check if user is asking what the bot can do"""
    capability_patterns = ["what can you", "what do you", "your capabilities", "can you help", 
                          "what can u", "what do u", "what you do"]
    q_lower = query.lower().strip()
    return any(p in q_lower for p in capability_patterns)

def is_simple_fest_query(query: str) -> bool:
    """Check if it's a simple 'what is brahma/ashwamedha' query"""
    q_lower = query.lower().strip()
    
    # Check for deep/complex question indicators first
    deep_keywords = ["history", "when started", "why called", "origin", "background", 
                     "story", "past", "previous", "earlier", "evolution", "tradition",
                     "how many", "who founded", "who started", "details about", "founded in"]
    
    if any(keyword in q_lower for keyword in deep_keywords):
        return False  # It's a deep question, needs semantic search
    
    # Remove common punctuation for easier matching
    q_normalized = q_lower.replace("?", "").replace("!", "").strip()
    
    # Just the fest name alone or with minimal words
    simple_patterns = [
        r"^bh?rama$",
        r"^ashwamedha$",
        r"^aswamedha$",
        r"^what is bh?rama",
        r"^what's bh?rama",
        r"^whats bh?rama",
        r"^tell me about bh?rama",
        r"^explain bh?rama",
        r"^about bh?rama",
        r"^what is ashwamedha",
        r"^what's ashwamedha",
        r"^whats ashwamedha",
        r"^tell me about ashwamedha",
        r"^explain ashwamedha",
        r"^about ashwamedha",
    ]
    
    for pattern in simple_patterns:
        if re.match(pattern, q_normalized):
            return True
    
    # If query is very short (1-3 words) and mentions fest, it's probably simple
    words = q_normalized.split()
    if len(words) <= 3:
        if any(fest in q_normalized for fest in ["brahma", "brama", "ashwamedha", "aswamedha"]):
            return True
    
    return False

def is_relevant_query(query: str) -> bool:
    """Quick relevance check with fuzzy matching and event name detection"""
    keywords = ["event", "brahma", "ashwamedha", "fest", "festival", "college", 
                "when", "where", "what", "date", "time", "venue", "asiet", "registration",
                "participate", "team", "prize", "competition", "workshop"]
    q_lower = query.lower()
    q_tokens = tokenize(q_lower)
    
    # Direct keyword match
    if any(kw in q_lower for kw in keywords):
        return True
    
    # Check if query matches any event name from cache (even partially)
    for event in EVENT_CACHE[:50]:  # Check first 50 events
        event_name = event.get("event_name", "").lower()
        if event_name:
            event_tokens = tokenize(event_name)
            # If ANY meaningful word from event name is in query
            common_tokens = event_tokens.intersection(q_tokens)
            if common_tokens:
                # Filter out very short words (like "a", "of", "the")
                meaningful_matches = [t for t in common_tokens if len(t) >= 3]
                if meaningful_matches:
                    return True
            # Or if event name appears as substring
            if len(event_name) > 4 and event_name in q_lower:
                return True
    
    # Fuzzy match for common misspellings
    for word in re.findall(r"\b[a-zA-Z]{4,}\b", q_lower):  # Words 4+ chars
        for kw in ["brahma", "ashwamedha", "event", "festival"]:
            if similarity(word, kw) >= 0.7:
                return True
    
    return False
def detect_event_category(query: str):
    q = query.lower()

    is_general = any(w in q for w in ["general", "fun", "games"])
    is_cultural = any(w in q for w in ["cultural", "dance", "music", "arts"])
    is_technical = any(w in q for w in ["technical", "tech", "coding", "hack"])

    fest = fuzzy_fest_match(query)  # brahma / ashwamedha / None

    return fest, is_general, is_cultural, is_technical

def is_event_list_query(query: str) -> bool:
    """Check if user is asking for a list of events"""
    q = query.lower()
    
    # Keywords that indicate user wants a list
    list_keywords = [
        "list of",
        "list events",
        "all events",
        "what are the events",
        "what are events",
        "which events",
        "show events",
        "show me",
        "show all",
        "tell me events",
        "tell me the events",
        "events in",
        "what events are",
        "what events",
        "give me events",
        "give me",
        "get events",
        "events list",
        "list all",
        "what all events"
    ]
    
    # Check if query contains event list keywords AND fest/event indicators
    has_list_keyword = any(keyword in q for keyword in list_keywords)
    has_event_indicator = "event" in q or "brahma" in q or "ashwamedha" in q or "ashwmedha" in q or "aswamedha" in q
    
    return has_list_keyword and has_event_indicator

# ---------------- MAIN CHAT ---------------- #

def chat(user_message: str) -> str:
    """
    Lightweight chat function with memory optimization.
    PRIORITY: Pleasantries → Simple Fest Info → Relevance Check → Events → Registration → Semantic Search
    """
    analytics = get_analytics()
    
    try:
        query = user_message.strip()
        if not query:
            return "Please ask a question."

        # 1. SECURITY: Handle meta questions and abuse first
        if is_meta_question(query):
            if analytics:
                analytics["pattern_matches"]["meta_question"] += 1
            return "I'm here specifically to help with Brahma '26 and Ashwamedha '26 event-related queries."
        if is_abusive_query(query):
            if analytics:
                analytics["pattern_matches"]["abuse"] += 1
            return random.choice(ABUSE_RESPONSES)
        
        # 2. PLEASANTRIES: Handle conversational elements early
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
        
        if is_okay(query):
            if analytics:
                analytics["pattern_matches"]["okay"] += 1
            return random.choice(OKAY_RESPONSES)
        
        # 3. FEST INFO: Simple "what is brahma/ashwamedha" queries (before complex matching)
        fest = fuzzy_fest_match(query)
        if fest and is_simple_fest_query(query):
            if analytics:
                analytics["pattern_matches"]["fest_info"] += 1
            if fest == "brahma":
                return random.choice(BRAHMA_RESPONSES)
            if fest == "ashwamedha":
                return random.choice(ASHWAMEDHA_RESPONSES)

        # 4. RELEVANCE CHECK: Early exit for irrelevant queries (before expensive operations)
        if not is_relevant_query(query):
            if analytics:
                analytics["pattern_matches"]["out_of_context"] += 1
            return random.choice(OUT_OF_CONTEXT_RESPONSES)
        
        # 5. PRIMARY PURPOSE: Event matching (fast, direct lookup)
        event = find_exact_event(query)
        if event:
            if analytics:
                analytics["event_matches"] += 1
            return format_event_response(event, query)
        
        # 6. EVENT LISTS: Check if user wants list of events
        if is_event_list_query(query):
            if analytics:
                analytics["pattern_matches"]["event_list"] += 1
            fest, is_general, is_cultural, is_technical = detect_event_category(query)

            if fest == "brahma":
                if is_general:
                    return format_event_list(
                        "Brahma '26 – General Events",
                        BRAHMA_GENERAL_EVENTS
                    )
                elif is_cultural:
                    return format_event_list(
                        "Brahma '26 – Cultural Events",
                        BRAHMA_CULTURAL_EVENTS
                    )
                elif is_technical:
                    return format_event_list(
                        "Brahma '26 – Technical Events",
                        BRAHMA_TECHNICAL_EVENTS
                    )
                else:
                    # All Brahma events
                    all_events = BRAHMA_GENERAL_EVENTS + BRAHMA_CULTURAL_EVENTS + BRAHMA_TECHNICAL_EVENTS
                    return format_event_list("Brahma '26 – All Events", all_events)

            elif fest == "ashwamedha":
                return format_event_list(
                    "Ashwamedha '26 – Technical Events",
                    ASHWAMEDHA_TECHNICAL_EVENTS
                )
            
            # If no fest detected but user asked for events, try to infer or show all
            else:
                # Show both festival events if no specific fest mentioned
                all_events = (
                    [f"🎉 BRAHMA '26 EVENTS:"] + BRAHMA_GENERAL_EVENTS + BRAHMA_CULTURAL_EVENTS + BRAHMA_TECHNICAL_EVENTS +
                    ["", "⚙️ ASHWAMEDHA '26 EVENTS:"] + ASHWAMEDHA_TECHNICAL_EVENTS
                )
                return format_event_list("ASIET Festivals", all_events)
        
        # 7. REGISTRATION: Important action queries
        if is_registration_query(query):
            if analytics:
                analytics["pattern_matches"]["registration"] += 1
            fest = fuzzy_fest_match(query)
            if fest == "brahma":
                return random.choice(BRAHMA_REGISTRATION_RESPONSES)
            if fest == "ashwamedha":
                return random.choice(ASHWAMEDHA_REGISTRATION_RESPONSES)
            # Fallback if fest not mentioned
            return (
                "Please specify the fest you want to register for.\n\n"
                "You can say:\n"
                "• Register for Brahma '26\n"
                "• Register for Ashwamedha '26"
            )

        # 8. SEMANTIC SEARCH: Complex queries (more expensive, used as last resort)
        try:
            if analytics:
                analytics["semantic_search_calls"] += 1
            
            results = semantic_search(query, top_k=2)  # Reduced to 2
            
            if not results:
                return "I don't have specific information about that. Try asking about events or festival details."

            # Build concise context
            context_parts = []
            for r in results[:2]:  # Use max 2 results
                text = r["text"][:300]  # Truncate
                context_parts.append(text)
            
            context = "\n".join(context_parts)
            
            # Generate answer
            if analytics:
                analytics["llm_calls"] += 1
            answer = generate_answer(context, query)
            
            # Cleanup
            gc.collect()
            
            return answer
            
        except Exception as e:
            print(f"❌ Search error: {e}")
            return "Sorry, I'm having trouble processing that request."

    except Exception as e:
        print(f"❌ Chat error: {e}")
        return "Sorry, something went wrong."

def format_event_response(event: dict, query: str = "") -> str:
    """Format event info with conversational response variations, optimized to answer only what's asked"""
    name = event.get("event_name", "Unknown Event")
    date = safe(event.get("date"))
    time = safe(event.get("time"))
    venue = safe(event.get("venue"))
    details = safe(event.get("details"), "")
    coordinator = format_names(event.get("coordinator"))
    phone = safe(event.get("phone_number"))
    fest = safe(event.get("fest"))
    slots = safe(event.get("slots"))
    poster = safe(event.get("poster"))
    amount = safe(event.get("amount"))
    category = safe(event.get("category"))
    
    q_lower = query.lower()
    
    # Detect what specific info is being asked
    asking_venue = any(word in q_lower for word in ["venue", "venu", "vanue", "vennue", "where", "wher", "were", "whre", "location", "lokation", "locaton", "loaction", "place", "plase", "plce", "held"])
    asking_time = any(word in q_lower for word in ["time", "tym", "tyme", "when", "wen", "whn", "start", "strt", "stat", "begin"])
    asking_date = any(word in q_lower for word in ["date", "dat", "dait", "day", "when", "wen", "whn"])
    asking_coordinator = any(word in q_lower for word in ["coordinator", "cordinator", "coordinater", "co-ordinator", "coordnator", "contact", "contct", "cantact", "contat", "who", "organize", "organise", "orgnaize", "organiz", "reach", "phone", "fone", "phon", "phn", "number", "nmbr", "numbr", "no", "num", "call", "mobile", "mobil", "moble", "organizer", "organiser", "organisor", "incharge", "in-charge"])
    asking_what = any(word in q_lower for word in ["what", "wat", "wht", "about", "abt", "abut", "detail", "details", "detial", "detal", "describe", "descibe", "descrbe"])
    asking_fest = any(word in q_lower for word in ["fest", "fst", "fiest", "festival", "festivel", "festivl", "festval", "occasion"])
    asking_slots = any(word in q_lower for word in ["slots", "sloat", "slts", "seats", "seets", "sats", "vacancy", "available", "availble", "avaiable", "avalable", "limit"])
    asking_poster = any(word in q_lower for word in ["poster", "postr", "pster", "image", "imge", "img", "picture", "pic", "pictur", "pict", "flyer"])
    asking_amount = any(word in q_lower for word in ["amount", "ammount", "amnt", "amt", "price", "pric", "prise", "fee", "fe", "fees", "cost", "cst", "coost", "registration", "registraton", "regestration", "charge", "charg", "chrg", "charges", "money", "pay", "payment", "payement", "paymnt", "paid", "rates", "pricing", "how much"])
    asking_category = any(word in q_lower for word in ["category", "categry", "catagory", "catgory", "type", "typ", "tipe", "kind", "genre"])
    
    # Count how many aspects are being asked
    aspects_count = sum([
        asking_venue, asking_time, asking_date, asking_coordinator, asking_what,
        asking_fest, asking_slots, asking_poster, asking_amount, asking_category
    ])
    
    # --- Single Aspect Logic ---
    
    # If only asking about venue
    if asking_venue and aspects_count == 1:
        responses = [
            f"{name} will be held at {venue}.",
            f"The venue for {name} is {venue}.",
            f"{name} is at {venue}.",
            f"You'll find {name} at {venue}.",
            f"The location is {venue} for {name}."
        ]
        return random.choice(responses)
    
    # If only asking about time
    if asking_time and not asking_date and aspects_count == 1:
        responses = [
            f"{name} starts at {time}.",
            f"The event begins at {time}.",
            f"{name} is scheduled for {time}.",
            f"It's at {time}.",
            f"The time is {time} for {name}."
        ]
        return random.choice(responses)
    
    # If only asking about date
    if asking_date and not asking_time and aspects_count == 1:
        responses = [
            f"{name} is on {date}.",
            f"The date is {date}.",
            f"It's happening on {date}.",
            f"{name} is scheduled for {date}.",
            f"Mark your calendar for {date}!"
        ]
        return random.choice(responses)

    # If only asking about amount
    if asking_amount and aspects_count == 1:
        return random.choice([
            f"The registration fee for {name} is {amount}.",
            f"It costs {amount} to participate in {name}.",
            f"The amount for {name} is {amount}.",
            f"{name} costs {amount}.",
            f"You'll need to pay {amount} for {name}.",
            f"The entry fee is {amount}."
        ])

    # If only asking about slots
    if asking_slots and aspects_count == 1:
        return random.choice([
            f"There are {slots} slots available for {name}.",
            f"{name} has {slots} seats left.",
            f"The slot limit for {name} is {slots}."
        ])

    # If only asking about poster
    if asking_poster and aspects_count == 1:
        if poster != "not specified":
            return f"You can check out the poster for {name} here: {poster}"
        return f"I'm sorry, the poster for {name} is not specified."

    # If only asking about category
    if asking_category and aspects_count == 1:
        return f"{name} is categorized as a {category} event."

    # If only asking about the fest
    if asking_fest and aspects_count == 1:
        return f"{name} is part of the {fest} festival."
    
    # If only asking about coordinator
    if asking_coordinator and aspects_count == 1:
        if coordinator != "not specified":
            phone_info = f" (Phone: {phone})" if phone != "not specified" else ""
            responses = [
                f"The coordinator for {name} is {coordinator}{phone_info}.",
                f"You can contact {coordinator}{phone_info} for {name}.",
                f"{coordinator} is coordinating {name}{phone_info}.",
                f"Reach out to {coordinator}{phone_info} for more details about {name}.",
                f"The point of contact is {coordinator}{phone_info}."
            ]
            return random.choice(responses)
        else:
            return f"Coordinator information is not available for {name}."
    
    # If asking what the event is about
    if asking_what and aspects_count == 1 and details:
        responses = [
            f"{name} - {details}",
            f"{name} is {details.lower()}",
            f"It's {details.lower()}",
            f"{details}",
            f"{name}: {details}"
        ]
        return random.choice(responses)
    
    # --- Two-Field Combinations ---

    # If asking about when (date + time)
    if asking_date and asking_time and aspects_count == 2:
        responses = [
            f"{name} is on {date} at {time}.",
            f"It's scheduled for {date} at {time}.",
            f"{name} happens on {date}, starting at {time}.",
            f"The event is on {date} at {time}.",
            f"Mark {date} at {time} for {name}!"
        ]
        return random.choice(responses)
    
    # Time combinations
    if asking_time and asking_venue and aspects_count == 2:
        return random.choice([
            f"{name} starts at {time} at {venue}.",
            f"{name} is scheduled at {time} in {venue}.",
            f"The event takes place at {venue} at {time}.",
            f"You can attend {name} at {venue} starting at {time}."
        ])

    if asking_time and asking_coordinator and aspects_count == 2:
        if coordinator != "not specified":
            phone_info = f" (Phone: {phone})" if phone != "not specified" else ""
            return random.choice([
                f"{name} starts at {time} and is coordinated by {coordinator}{phone_info}.",
                f"The event begins at {time}. Coordinators: {coordinator}{phone_info}.",
                f"{coordinator} are coordinating {name}, which starts at {time}. Contact: {phone if phone != 'not specified' else 'N/A'}.",
                f"You can attend {name} at {time}. The coordinators are {coordinator}{phone_info}."
            ])
        else:
            return f"{name} starts at {time}, but coordinator details are not available."

    if asking_time and asking_fest and aspects_count == 2:
        return random.choice([
            f"{name} starts at {time} as part of {fest}.",
            f"The event is at {time} during {fest}.",
            f"{name} is scheduled for {time} in the {fest} festival.",
            f"You can catch {name} at {time} during {fest}."
        ])

    if asking_time and asking_poster and aspects_count == 2:
        if poster != "not specified":
            return random.choice([
                f"{name} starts at {time}. Check the poster: {poster}",
                f"The event is at {time}. Poster here: {poster}",
                f"{name} begins at {time}. View poster: {poster}"
            ])
        return f"{name} starts at {time}, but the poster is not available."

    if asking_time and asking_amount and aspects_count == 2:
        return random.choice([
            f"{name} starts at {time} with a registration fee of {amount}.",
            f"The event is at {time} and costs {amount} to register.",
            f"{name} begins at {time}. Fee: {amount}.",
            f"It's scheduled for {time} and the fee is {amount}.",
            f"{name} happens at {time}. You'll need to pay {amount}.",
            f"The event starts at {time} with an entry fee of {amount}."
        ])

    if asking_time and asking_category and aspects_count == 2:
        return random.choice([
            f"{name} is a {category} event starting at {time}.",
            f"This {category} event begins at {time}.",
            f"{name} ({category}) is scheduled for {time}."
        ])

    if asking_time and asking_slots and aspects_count == 2:
        return random.choice([
            f"{name} starts at {time} with {slots} slots available.",
            f"The event is at {time} and has {slots} seats.",
            f"{name} begins at {time}. Slots: {slots}."
        ])

    # Date combinations
    if asking_date and asking_venue and aspects_count == 2:
        return random.choice([
            f"{name} is happening on {date} at {venue}.",
            f"The event will be held at {venue} on {date}.",
            f"{name} takes place on {date} in {venue}.",
            f"On {date}, {name} will be conducted at {venue}."
        ])

    if asking_date and asking_what and aspects_count == 2 and details:
        return random.choice([
            f"{name} is on {date}. {details}",
            f"On {date}, {name} - {details}",
            f"{name} happens on {date}. It's {details.lower()}",
            f"{details} The event is on {date}."
        ])

    if asking_date and asking_coordinator and aspects_count == 2:
        if coordinator != "not specified":
            phone_info = f" (Phone: {phone})" if phone != "not specified" else ""
            return random.choice([
                f"{name} is on {date}. Coordinator: {coordinator}{phone_info}.",
                f"The event is on {date}, coordinated by {coordinator}{phone_info}.",
                f"{name} happens on {date}. Contact {coordinator} at {phone if phone != 'not specified' else 'coordinator'} for details.",
                f"On {date}, {name} will be organized by {coordinator}{phone_info}."
            ])
        return f"{name} is on {date}, but coordinator details are not available."

    if asking_date and asking_fest and aspects_count == 2:
        return random.choice([
            f"{name} is on {date} as part of {fest}.",
            f"The event is on {date} during {fest}.",
            f"{name} happens on {date} in the {fest} festival.",
            f"Mark {date} for {name} during {fest}!"
        ])

    if asking_date and asking_slots and aspects_count == 2:
        return random.choice([
            f"{name} is on {date} with {slots} slots available.",
            f"The event is on {date} and has {slots} seats.",
            f"{name} happens on {date}. Slots: {slots}."
        ])

    if asking_date and asking_poster and aspects_count == 2:
        if poster != "not specified":
            return random.choice([
                f"{name} is on {date}. Check the poster: {poster}",
                f"The event is on {date}. Poster here: {poster}",
                f"Mark {date}! Poster: {poster}"
            ])
        return f"{name} is on {date}, but the poster is not available."

    if asking_date and asking_amount and aspects_count == 2:
        return random.choice([
            f"{name} is on {date} with a registration fee of {amount}.",
            f"The event is on {date} and costs {amount}.",
            f"{name} happens on {date}. Fee: {amount}.",
            f"It's scheduled for {date}. The fee is {amount}.",
            f"On {date}, {name} will take place with an entry fee of {amount}.",
            f"Mark {date}! Registration costs {amount}."
        ])

    if asking_date and asking_category and aspects_count == 2:
        return random.choice([
            f"{name} is a {category} event happening on {date}.",
            f"This {category} event is on {date}.",
            f"{name} ({category}) is scheduled for {date}."
        ])

    # Coordinator combinations
    if asking_coordinator and asking_venue and aspects_count == 2:
        if coordinator != "not specified":
            phone_info = f" (Phone: {phone})" if phone != "not specified" else ""
            return random.choice([
                f"{name} will be held at {venue} and is coordinated by {coordinator}{phone_info}.",
                f"The venue for {name} is {venue}. Coordinators: {coordinator}{phone_info}.",
                f"{coordinator} are coordinating {name}, which will take place at {venue}. Contact: {phone if phone != 'not specified' else 'N/A'}.",
                f"You can find {name} at {venue}. The coordinators are {coordinator}{phone_info}."
            ])
        else:
            return f"{name} will be held at {venue}, but coordinator details are not available."

    if asking_coordinator and asking_fest and aspects_count == 2:
        if coordinator != "not specified":
            phone_info = f" (Phone: {phone})" if phone != "not specified" else ""
            return random.choice([
                f"{name} is part of {fest}, coordinated by {coordinator}{phone_info}.",
                f"{coordinator} are organizing {name} during {fest}. Contact: {phone if phone != 'not specified' else 'N/A'}.",
                f"The {fest} event {name} is coordinated by {coordinator}{phone_info}.",
                f"{name} ({fest}) - Coordinator: {coordinator}{phone_info}."
            ])
        return f"{name} is part of {fest}, but coordinator details are not available."

    if asking_coordinator and asking_slots and aspects_count == 2:
        if coordinator != "not specified":
            phone_info = f" (Phone: {phone})" if phone != "not specified" else ""
            return random.choice([
                f"{name} has {slots} slots. Coordinator: {coordinator}{phone_info}.",
                f"There are {slots} seats available. Contact {coordinator} at {phone if phone != 'not specified' else 'coordinator'} for {name}.",
                f"{coordinator} are coordinating {name}, which has {slots} slots. Phone: {phone if phone != 'not specified' else 'N/A'}.",
                f"{name} - {slots} slots available. Reach out to {coordinator}{phone_info}."
            ])
        return f"{name} has {slots} slots, but coordinator details are not available."

    if asking_coordinator and asking_poster and aspects_count == 2:
        phone_info = f" (Phone: {phone})" if phone != "not specified" else ""
        if coordinator != "not specified" and poster != "not specified":
            return random.choice([
                f"{name} is coordinated by {coordinator}{phone_info}. Poster: {poster}",
                f"Contact {coordinator} at {phone if phone != 'not specified' else 'coordinator'} for {name}. Check poster: {poster}",
                f"Coordinator: {coordinator}{phone_info}. View poster here: {poster}"
            ])
        elif coordinator != "not specified":
            return f"{name} is coordinated by {coordinator}{phone_info}, but the poster is not available."
        return f"The poster is available at {poster}, but coordinator details are not specified."

    if asking_coordinator and asking_amount and aspects_count == 2:
        if coordinator != "not specified":
            phone_info = f" (Phone: {phone})" if phone != "not specified" else ""
            return random.choice([
                f"{name} has a registration fee of {amount}. Coordinator: {coordinator}{phone_info}.",
                f"The fee is {amount}. Contact {coordinator} at {phone if phone != 'not specified' else 'coordinator'} for {name}.",
                f"{coordinator} are coordinating {name}, which costs {amount}. Phone: {phone if phone != 'not specified' else 'N/A'}.",
                f"{name} - Fee: {amount}. Reach out to {coordinator}{phone_info}.",
                f"It costs {amount}. You can contact {coordinator}{phone_info} for more details.",
                f"{coordinator} are organizing {name}. The registration fee is {amount}. Contact: {phone if phone != 'not specified' else 'N/A'}."
            ])
        return f"{name} costs {amount}, but coordinator details are not available."

    if asking_coordinator and asking_category and aspects_count == 2:
        if coordinator != "not specified":
            phone_info = f" (Phone: {phone})" if phone != "not specified" else ""
            return random.choice([
                f"{name} is a {category} event coordinated by {coordinator}{phone_info}.",
                f"This {category} event is organized by {coordinator}{phone_info}.",
                f"{coordinator} are coordinating {name} ({category}). Contact: {phone if phone != 'not specified' else 'N/A'}.",
                f"{name} ({category}) - Coordinator: {coordinator}{phone_info}."
            ])
        return f"{name} is a {category} event, but coordinator details are not available."

    # Venue combinations
    if asking_venue and asking_fest and aspects_count == 2:
        return random.choice([
            f"{name} will be held at {venue} during {fest}.",
            f"The venue is {venue} for this {fest} event.",
            f"{name} ({fest}) takes place at {venue}.",
            f"You can find {name} at {venue} during {fest}."
        ])

    if asking_venue and asking_slots and aspects_count == 2:
        return random.choice([
            f"{name} will be held at {venue} with {slots} slots available.",
            f"The venue is {venue} and there are {slots} seats.",
            f"{name} is at {venue}. Slots: {slots}."
        ])

    if asking_venue and asking_poster and aspects_count == 2:
        if poster != "not specified":
            return random.choice([
                f"{name} will be held at {venue}. Poster: {poster}",
                f"The venue is {venue}. Check poster: {poster}",
                f"{name} is at {venue}. View poster here: {poster}"
            ])
        return f"{name} will be held at {venue}, but the poster is not available."

    if asking_venue and asking_amount and aspects_count == 2:
        return random.choice([
            f"{name} will be held at {venue} with a registration fee of {amount}.",
            f"The venue is {venue} and the fee is {amount}.",
            f"{name} is at {venue}. Fee: {amount}.",
            f"It's happening at {venue}. The cost is {amount}.",
            f"{name} takes place at {venue} with an entry fee of {amount}.",
            f"You can attend {name} at {venue} for {amount}."
        ])

    if asking_venue and asking_category and aspects_count == 2:
        return random.choice([
            f"{name} is a {category} event held at {venue}.",
            f"This {category} event takes place at {venue}.",
            f"{name} ({category}) will be at {venue}."
        ])

    if asking_venue and asking_what and aspects_count == 2 and details:
        return random.choice([
            f"{name} will be held at {venue}. {details}",
            f"The venue is {venue}. {details}",
            f"{name} is at {venue}. It's {details.lower()}"
        ])

    # Fest combinations
    if asking_fest and asking_slots and aspects_count == 2:
        return random.choice([
            f"{name} is part of {fest} with {slots} slots available.",
            f"This {fest} event has {slots} seats.",
            f"{name} ({fest}) - Slots: {slots}."
        ])

    if asking_fest and asking_poster and aspects_count == 2:
        if poster != "not specified":
            return random.choice([
                f"{name} is part of {fest}. Poster: {poster}",
                f"This {fest} event's poster: {poster}",
                f"{name} ({fest}) - View poster: {poster}"
            ])
        return f"{name} is part of {fest}, but the poster is not available."

    if asking_fest and asking_amount and aspects_count == 2:
        return random.choice([
            f"{name} is part of {fest} with a registration fee of {amount}.",
            f"This {fest} event costs {amount}.",
            f"{name} ({fest}) - Fee: {amount}.",
            f"It's a {fest} event with an entry fee of {amount}.",
            f"{name} happens during {fest}. The fee is {amount}.",
            f"You can participate in {name} at {fest} for {amount}."
        ])

    if asking_fest and asking_category and aspects_count == 2:
        return random.choice([
            f"{name} is a {category} event in {fest}.",
            f"This {category} event is part of {fest}.",
            f"{name} ({category}) happens during {fest}."
        ])

    if asking_fest and asking_what and aspects_count == 2 and details:
        return random.choice([
            f"{name} is part of {fest}. {details}",
            f"This {fest} event: {details}",
            f"{name} ({fest}) - {details}"
        ])

    # Slots combinations
    if asking_slots and asking_poster and aspects_count == 2:
        if poster != "not specified":
            return random.choice([
                f"{name} has {slots} slots. Poster: {poster}",
                f"There are {slots} seats available. Check poster: {poster}",
                f"{name} - Slots: {slots}. View poster: {poster}"
            ])
        return f"{name} has {slots} slots, but the poster is not available."

    if asking_slots and asking_amount and aspects_count == 2:
        return random.choice([
            f"{name} has {slots} slots with a registration fee of {amount}.",
            f"There are {slots} seats available for {amount}.",
            f"{name} - Fee: {amount}, Slots: {slots}.",
            f"It costs {amount} and has {slots} slots available.",
            f"{name} has {slots} spots left. The entry fee is {amount}.",
            f"Registration is {amount} with {slots} seats remaining."
        ])

    if asking_slots and asking_category and aspects_count == 2:
        return random.choice([
            f"{name} is a {category} event with {slots} slots available.",
            f"This {category} event has {slots} seats.",
            f"{name} ({category}) - Slots: {slots}."
        ])

    if asking_slots and asking_what and aspects_count == 2 and details:
        return random.choice([
            f"{name} has {slots} slots. {details}",
            f"There are {slots} seats available. {details}",
            f"{name} - Slots: {slots}. {details}"
        ])

    # Poster combinations
    if asking_poster and asking_amount and aspects_count == 2:
        if poster != "not specified":
            return random.choice([
                f"{name} costs {amount}. Poster: {poster}",
                f"Registration fee: {amount}. Check poster: {poster}",
                f"{name} - Fee: {amount}. View poster: {poster}",
                f"The entry fee is {amount}. View the poster here: {poster}",
                f"It's {amount} to register. Check out the poster: {poster}",
                f"{name} has a fee of {amount}. Poster available at: {poster}"
            ])
        return f"{name} costs {amount}, but the poster is not available."

    if asking_poster and asking_category and aspects_count == 2:
        if poster != "not specified":
            return random.choice([
                f"{name} is a {category} event. Poster: {poster}",
                f"This {category} event's poster: {poster}",
                f"{name} ({category}) - View poster: {poster}"
            ])
        return f"{name} is a {category} event, but the poster is not available."

    if asking_poster and asking_what and aspects_count == 2 and details:
        if poster != "not specified":
            return random.choice([
                f"{name} - {details} Poster: {poster}",
                f"{details} Check poster: {poster}",
                f"{name}: {details} View poster: {poster}"
            ])
        return f"{name} - {details} But the poster is not available."

    # Amount combinations
    if asking_amount and asking_category and aspects_count == 2:
        return random.choice([
            f"{name} is a {category} event with a registration fee of {amount}.",
            f"This {category} event costs {amount}.",
            f"{name} ({category}) - Fee: {amount}.",
            f"It's a {category} event. The fee is {amount}.",
            f"{name} falls under {category} and costs {amount}.",
            f"This {category} event has an entry fee of {amount}."
        ])

    if asking_amount and asking_what and aspects_count == 2 and details:
        return random.choice([
            f"{name} costs {amount}. {details}",
            f"Registration fee: {amount}. {details}",
            f"{name} - Fee: {amount}. {details}",
            f"The entry fee is {amount}. {details}",
            f"{details} It costs {amount} to participate.",
            f"{name} has a fee of {amount}. {details}"
        ])

    # Category combinations
    if asking_category and asking_what and aspects_count == 2 and details:
        return random.choice([
            f"{name} is a {category} event. {details}",
            f"This {category} event: {details}",
            f"{name} ({category}) - {details}"
        ])

    # --- Three-Field Combinations ---

    # Logistics (Amount + Venue + Date)
    if asking_amount and asking_venue and asking_date and aspects_count == 3:
        return f"{name} is on {date} at {venue} with a registration fee of {amount}."

    # Registration (Amount + Slots)
    if asking_amount and asking_slots and aspects_count == 2:
        return f"For {name}, the registration fee is {amount} and there are {slots} slots available."

    # Event Details (Category + Fest)
    if asking_category and asking_fest and aspects_count == 2:
        return f"{name} is a {category} event happening during {fest}."

    # Full technical details (Amount + Slots + Category + Coordinator)
    if asking_amount and asking_slots and asking_category and asking_coordinator and aspects_count == 4:
        return f"{name} ({category}): The fee is {amount} for {slots} slots. Coordinator: {coordinator}."
    
    # Default: Full information with conversational variations
    phone_info = f" (Phone: {phone})" if phone != "not specified" else ""
    templates = [
        f"{name} is a {category} event happening on {date} at {time} at {venue} as part of {fest}. Fee: {amount}. Slots: {slots}. {details}" + 
        (f" You can contact {coordinator}{phone_info} for more details." if coordinator != "not specified" else ""),
        
        f"Sure! {name} is a {category} event in {fest} scheduled for {date} at {time}. {details} Venue: {venue}. Amount: {amount}." +
        (f" For more info, reach out to {coordinator}." if coordinator != "not specified" else ""),
        
        f"{name} will be held on {date} at {time} at {venue}. This {category} event has {slots} slots and a fee of {amount}. {details}" +
        (f" If you have questions, contact {coordinator}." if coordinator != "not specified" else ""),
        
        f"Great question! {name} takes place on {date} at {time}. {details} Category: {category}. It's being held at {venue}." +
        (f" The coordinator is {coordinator}." if coordinator != "not specified" else ""),
        
        f"{name} is on {date} at {time}, venue is {venue}. This {fest} event costs {amount}. {details}" +
        (f" Get in touch with {coordinator} if you need more info." if coordinator != "not specified" else ""),
        
        f"{name} - {details} Category: {category}. Scheduled for {date} at {time}. Location: {venue}. Fee: {amount}." +
        (f" Contact: {coordinator}." if coordinator != "not specified" else "")
    ]
    
    return random.choice(templates)
