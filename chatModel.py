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
        self.llm = OpenAI (
            temperature=0.7,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        