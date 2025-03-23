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
            return False, "I couldn't understand that time format. Please try again."
        
        
        