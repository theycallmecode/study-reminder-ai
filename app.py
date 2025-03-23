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


@app.route('/')
def index():
    """Render the main chat interface"""
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    """Render the reminders dashboard"""
    reminders = reminder_manager.get_upcoming_reminders()
    return render_template('dashboard.html', reminders=reminders)