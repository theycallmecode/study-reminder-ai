# main application file

from flask import Flask, render_template, request, jsonify, redirect, url_for
from chat_model import StudyBotAI
from reminder_manager import ReminderManager
import os
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize components
chatbot = StudyBotAI()
reminder_manager = ReminderManager()