from flask import Flask, request, render_template, jsonify
import threading
from reminder_manager import ReminderManager
from chat_model import ChatModel

app = Flask(__name__)

# Initialize components
reminder_manager = ReminderManager()
chat_model = ChatModel()

# Run reminders in a separate thread
def run_reminders():
    reminder_manager.start()

threading.Thread(target=run_reminders, daemon=True).start()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    reminders = reminder_manager.get_reminders()
    return render_template('dashboard.html', reminders=reminders)

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    response = chat_model.get_response(user_message)
    
    # Check if user wants to set a reminder
    if "remind me" in user_message.lower():
        parts = user_message.lower().split("to")
        if len(parts) > 1:
            task = parts[1].strip()
            reminder_manager.add_reminder(task)
            return jsonify({"response": f"Reminder set for: {task}"})
    
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)