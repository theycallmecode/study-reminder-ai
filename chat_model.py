from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

# Initialize the OpenAI model
llm = OpenAI(api_key=api_key, temperature=0.7)

# Define a prompt template for study-related responses
prompt = PromptTemplate(
    input_variables=["user_input"],
    template="""
    You are a Study Reminder AI designed to help students. Your tone is friendly and encouraging.
    If the user asks about study tips, schedules, or reminders, provide helpful advice.
    If the user asks something unrelated, gently steer them back to studying.
    Respond to this: {user_input}
    """
)

def get_study_response(user_input):
    # Combine prompt with user input and get AI response
    formatted_prompt = prompt.format(user_input=user_input)
    response = llm(formatted_prompt)
    return response.strip()