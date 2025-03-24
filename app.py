from flask import Flask, request, render_template, jsonify, session
from flask_session import Session
import threading
from reminder_manager import ReminderManager
from chat_model import ChatModel
from datetime import datetime
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-here')
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Initialize components
reminder_manager = ReminderManager()
chat_model = ChatModel()

# Run reminders in a separate thread
def run_reminders():
    reminder_manager.start()

threading.Thread(target=run_reminders, daemon=True).start()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        username = request.form.get('username')
        if username:
            session['username'] = username
    username = session.get('username', None)
    greeting = chat_model.get_greeting(username) if username else None
    return render_template('index.html', username=username, greeting=greeting)

@app.route('/dashboard')
def dashboard():
    username = session.get('username', None)
    reminders = reminder_manager.get_reminders()
    return render_template('dashboard.html', reminders=reminders, username=username)

@app.route('/stopwatch')
def stopwatch():
    username = session.get('username', None)
    return render_template('stopwatch.html', username=username)

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    username = session.get('username', None)
    response = chat_model.get_response(user_message, username)
    
    if "remind me" in user_message.lower():
        parts = user_message.lower().split("to")
        if len(parts) > 1:
            task = parts[1].strip()
            reminder_manager.add_reminder(task)
            return jsonify({"response": f"Reminder set for: {task} (in 5 minutes)"})
    
    return jsonify({"response": response})

@app.route('/set_reminder', methods=['POST'])
def set_reminder():
    task = request.json.get('task')
    time_str = request.json.get('time')
    reminder_manager.add_reminder_with_time(task, time_str)
    return jsonify({"response": f"Reminder set for '{task}' at {time_str}"})

if __name__ == "__main__":
    port = int(os.getenv('PORT', 10000))  # Use Render's default port 10000
    host = '0.0.0.0'  # Bind to all interfaces
    logger.info(f"Starting Flask app on {host}:{port}")
    app.run(host=host, port=port, debug=False)