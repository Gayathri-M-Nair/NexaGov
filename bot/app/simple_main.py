from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.simple_chat import simple_chat

app = FastAPI(
    title="Kerala Schemes Chatbot",
    description="Simple chatbot for Kerala government schemes",
    version="1.0"
)

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

@app.get("/")
def health_check():
    return {"status": "healthy", "message": "Kerala Schemes Chatbot is running"}

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(req: ChatRequest):
    """Chat endpoint"""
    try:
        answer = simple_chat(req.message)
        return {"reply": answer}
    except Exception as e:
        print(f"Error: {e}")
        return {"reply": "Sorry, something went wrong. Please try again."}
