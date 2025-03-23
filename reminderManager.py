# handle scheduling function and reminder

import schedule
import time
import threading
import datetime
import json
import os
from datetime import datetime, timedelta
import pyttsx3


class ReminderManager:
    def __init__(self):
        # Initialize storage for reminders
        self.reminders = []
        self.load_reminders()
        
        # Initialize text-to-speech engine for notifications
        self.tts_engine = pyttsx3.init()
        
        # Start the scheduler in a separate thread
        self.scheduler_thread = threading.Thread(target=self.run_scheduler)
        self.scheduler_thread.daemon = True
        self.scheduler_thread.start()


    def load_reminders(self):
        """Load reminders from storage"""
        try:
            if os.path.exists('reminders.json'):
                with open('reminders.json', 'r') as f:
                    self.reminders = json.load(f)
        except Exception as e:
            print(f"Error loading reminders: {e}")
    

    def save_reminders(self):
        """Save reminders to storage"""
        try:
            with open('reminders.json', 'w') as f:
                json.dump(self.reminders, f, indent=2)
        except Exception as e:
            print(f"Error saving reminders: {e}")
    

    def add_reminder(self, task, subject, reminder_time, duration=None, priority="medium"):
        """Add a new study reminder"""
        # Parse the reminder time
        reminder_datetime = self._parse_time(reminder_time)
        if not reminder_datetime:
            return False, "I couldn't understand the time format. Please try again."
        
        # Generate a unique ID for the reminder
        reminder_id = str(len(self.reminders) + 1)
        
        # Create the reminder object
        reminder = {
            "id": reminder_id,
            "task": task,
            "subject": subject,
            "datetime": reminder_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            "duration": duration,
            "priority": priority,
            "completed": False,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Add to our list
        self.reminders.append(reminder)
        
        # Save to storage
        self.save_reminders()
        
        # Schedule the reminder
        self._schedule_reminder(reminder)
        
        return True, f"Reminder set for {task} ({subject}) at {reminder_datetime.strftime('%A, %B %d at %I:%M %p')}"
    
        
