class ChatModel:
    def __init__(self):
        self.responses = {
            "hello": "Hi there! How can I help you study today?",
            "thanks": "You're welcome! Keep up the good work!",
            "how are you": "I'm great, thanks! Ready to help you ace your studies."
        }

    def get_response(self, message):
        message = message.lower().strip()
        
        # Check predefined responses
        for key in self.responses:
            if key in message:
                return self.responses[key]
        
        # Default response
        return "I'm here to help! You can ask me to set study reminders or chat about your goals."