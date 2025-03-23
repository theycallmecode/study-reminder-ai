# main application file

from flask import Flask, render_template, request, jsonify, redirect, url_for
from chatModel import StudyBotAI
from reminderManager import ReminderManager
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


@app.route('/chat', methods=['POST'])
def chat():
    """Process user messages and return bot responses"""
    user_message = request.json.get('message', '')
    
    if not user_message:
        return jsonify({'response': 'Please enter a message'})
    
    # Get response from AI model
    response = chatbot.get_response(user_message)
    
    # Check if the message contains study reminder intent

    if any(keyword in user_message.lower() for keyword in ['remind', 'schedule', 'study', 'assignment', 'due']):
        # Extract study info
        study_info = chatbot.extract_study_info(user_message)
        
        if study_info.get('task') and study_info.get('datetime'):
            # Add the reminder
            success, reminder_msg = reminder_manager.add_reminder(
                task=study_info.get('task'),
                subject=study_info.get('subject', 'General Study'),
                reminder_time=study_info.get('datetime'),
                duration=study_info.get('duration'),
                priority=study_info.get('priority', 'medium')
            )
            
            if success:
                response += f"\n\n✅ {reminder_msg}"
            else:
                response += f"\n\n❌ {reminder_msg}"
    
    return jsonify({'response': response})


@app.route('/reminders', methods=['GET'])
def get_reminders():
    """API endpoint to get upcoming reminders"""
    reminders = reminder_manager.get_upcoming_reminders()
    return jsonify({'reminders': reminders})


@app.route('/complete-reminder/<reminder_id>', methods=['POST'])
def complete_reminder(reminder_id):
    """Mark a reminder as completed"""
    success = reminder_manager.mark_completed(reminder_id)
    if success:
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'error', 'message': 'Reminder not found'})


if __name__ == '__main__':
    app.run(debug=True)