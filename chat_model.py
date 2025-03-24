class ChatModel:
    def __init__(self):
        self.responses = {
            "hello": "Hi! How can I assist you with your studies today?",
            "thanks": "You're welcome! Keep pushing forward!",
            "how are you": "I'm doing awesome, thanks! How about you?"
        }

    def get_greeting(self, username):
        return f"Hello, {username}! Let's work even harder today!"

    def get_response(self, message, username=None):
        message = message.lower().strip()
        
        # Check predefined responses
        for key in self.responses:
            if key in message:
                return self.responses[key]
        
        # Default response with username if available
        if username:
            return f"Hey {username}, I'm here to help! You can ask me to set study reminders or chat about your goals."
        return "I'm here to help! You can ask me to set study reminders or chat about your goals."