from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from chat_model import get_study_response
from reminder_manager import schedule_reminder, run_scheduler

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Home route - displays the chat interface
@app.route('/')
def index():
    return render_template('index.html')

# Dashboard route - shows scheduled reminders
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# Chat endpoint - handles user messages
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    response = get_study_response(user_message)
    return jsonify({'response': response})

# Reminder endpoint - schedules a reminder
@app.route('/set_reminder', methods=['POST'])
def set_reminder():
    time = request.json.get('time')  # Expected format: HH:MM (e.g., "14:30")
    task = request.json.get('task')
    schedule_reminder(time, task)
    return jsonify({'status': 'Reminder set for ' + time})

if __name__ == '__main__':
    # Start the reminder scheduler in a separate thread
    import threading
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
    
    # Run Flask app
    app.run(debug=True)