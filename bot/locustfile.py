from locust import HttpUser, task, between
import json

class BrahmaChatUser(HttpUser):
    """
    Load test for Brahma Lite Chatbot
    Tests if the system crashes under load
    """
    
    # Wait 1-3 seconds between requests
    wait_time = between(1, 3)
    
    # Test questions
    questions = [
        "what is bhrahma",
        "what is aswamedha",
        "bhrahma",
        "hai"
    ]
    
    def on_start(self):
        """Called when a user starts"""
        print(f"🚀 User {self.environment.runner.user_count} started")
    
    @task(5)  # Higher weight - 5x more frequent
    def chat_with_questions(self):
        """Test chat endpoint with predefined questions"""
        import random
        question = random.choice(self.questions)
        
        with self.client.post(
            "/chat",
            json={"message": question},
            catch_response=True,
            name="POST /chat"
        ) as response:
            try:
                if response.status_code == 200:
                    data = response.json()
                    reply = data.get("reply", "")
                    
                    # Check for error responses
                    if "something went wrong" in reply.lower():
                        response.failure(f"Error response: {reply[:100]}")
                    elif "out of context" in reply.lower() and question in ["what is bhrahma", "bhrahma"]:
                        response.failure(f"Unexpected out-of-context for: {question}")
                    else:
                        response.success()
                else:
                    response.failure(f"Status code: {response.status_code}")
            except Exception as e:
                response.failure(f"Exception: {e}")
    
    @task(2)  # Medium weight
    def health_check(self):
        """Test health endpoint"""
        with self.client.get(
            "/",
            catch_response=True,
            name="GET /"
        ) as response:
            try:
                if response.status_code == 200:
                    data = response.json()
                    if data.get("status") == "healthy":
                        response.success()
                    else:
                        response.failure("Server not healthy")
                else:
                    response.failure(f"Status code: {response.status_code}")
            except Exception as e:
                response.failure(f"Exception: {e}")
    
    @task(1)  # Lower weight
    def stats_check(self):
        """Test stats endpoint"""
        with self.client.get(
            "/stats",
            catch_response=True,
            name="GET /stats"
        ) as response:
            try:
                if response.status_code == 200:
                    data = response.json()
                    if "cached_events" in data:
                        response.success()
                    else:
                        response.failure("Invalid stats response")
                else:
                    response.failure(f"Status code: {response.status_code}")
            except Exception as e:
                response.failure(f"Exception: {e}")
    
    @task(3)  # Medium-high weight
    def chat_with_events(self):
        """Test event-related questions"""
        event_questions = [
            "when is theme show",
            "tell me about choreo night",
            "what events are there",
            "venue for events"
        ]
        
        import random
        question = random.choice(event_questions)
        
        with self.client.post(
            "/chat",
            json={"message": question},
            catch_response=True,
            name="POST /chat (events)"
        ) as response:
            try:
                if response.status_code == 200:
                    response.success()
                else:
                    response.failure(f"Status code: {response.status_code}")
            except Exception as e:
                response.failure(f"Exception: {e}")
    
    def on_stop(self):
        """Called when a user stops"""
        print(f"🛑 User stopped")


# You can also create specific test scenarios
class StressTestUser(HttpUser):
    """
    More aggressive stress test
    """
    wait_time = between(0.5, 1)  # Faster requests
    
    @task
    def rapid_chat(self):
        """Send rapid chat requests"""
        with self.client.post(
            "/chat",
            json={"message": "bhrahma"},
            catch_response=True
        ) as response:
            if response.status_code != 200:
                response.failure(f"Status: {response.status_code}")
            else:
                response.success()
