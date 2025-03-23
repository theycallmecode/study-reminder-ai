import os
from dotenv import load_dotenv
from langchain.llms import OpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

# Load environment variables
load_dotenv()


class StudyBotAI:
    def __init__(self):
        # Initialize the language model
        self.llm = OpenAI(
            temperature=0.7,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        
        # Set up conversation memory
        self.memory = ConversationBufferMemory()
        
        # Create conversation chain
        self.conversation = ConversationChain(
            llm=self.llm,
            memory=self.memory,
            verbose=True
        )
        

    def get_response(self, user_input):
        """Process user input and return AI response"""
        
        # Create a study-focused system prompt
        system_prompt = """
        You are StudyHelper, an AI assistant focused on helping students with their studies.
        Your primary goals are to :
        1. Help students create and maintain study schedules
        2. Send timely reminders for study sessions and assignments
        3. Provide motivation and study tips
        4. Answer questions about study material when possible
        
        Be concise, encouraging, and practical in your responses.
        """
        

        # Combine system prompt with user input
        full_prompt = f"{system_prompt}\n\nStudent: {user_input}\nStudyBuddy:"
        
        try:
            # Get response from conversation chain
            response = self.conversation.predict(input=full_prompt)
            return response
        except Exception as e:
            print(f"Error getting AI response: {e}")
            return "I'm having trouble processing that. Please you try again."
        

    def extract_study_info(self, user_input):
        """
        Extract study-related information from user input
        Returns a dictionary with potential study task, subject, and time
        """
        extraction_prompt = f"""
        Extract the following information from this student input:
        
        Input: "{user_input}"
        
        Extract and return as JSON:
        1. task: The study task or assignment mentioned
        2. subject: The subject area
        3. datetime: When this needs to be done
        4. duration: How long they plan to study
        5. priority: High, medium, or low priority
        
        If any field is not mentioned, leave it as null.
        """
        
        try:
            response = self.llm.predict(extraction_prompt)

            # In real application, parse the JSON here
            # For simplicity, we'll return a sample dictionary
            # This would be replaced with actual parsing in production

            extracted_info = {
                "task": "study calculus",
                "subject": "math",
                "datetime": "tomorrow at 3pm",
                "duration": "2 hours",
                "priority": "high"
            }

            return extracted_info
        

        except Exception as e:

            print(f"Error extracting study info: {e}")
            return {}