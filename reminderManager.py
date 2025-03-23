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
    

    def get_upcoming_reminders(self, limit=5):
        """Get the next few upcoming reminders"""
        # Filter incomplete reminders and sort by date
        upcoming = [r for r in self.reminders if not r.get("completed", False)]
        upcoming.sort(key=lambda x: datetime.strptime(x["datetime"], "%Y-%m-%d %H:%M:%S"))
        
        # Return the next 'limit' reminders
        return upcoming[:limit]
    
    def mark_completed(self, reminder_id):
        """Mark a reminder as completed"""
        for reminder in self.reminders:
            if reminder["id"] == reminder_id:
                reminder["completed"] = True
                self.save_reminders()
                return True
        return False
    
    def send_reminder(self, reminder):
        """Send a notification for a reminder"""
        message = f"Reminder: Time to {reminder['task']} for {reminder['subject']}"
        print("\n" + "="*50)
        print(message)
        print("="*50 + "\n")
        
        # Use text-to-speech for desktop notification
        self.tts_engine.say(message)
        self.tts_engine.runAndWait()
        
        # In a real application, you might send this via email, SMS, or push notification
    
    def _parse_time(self, time_string):
        """Parse a time string into a datetime object"""
        now = datetime.now()
        
        # Handle common time formats - in a real app, you'd use a more robust parser
        try:
            # Simple formats like "tomorrow at 3pm"
            if "tomorrow" in time_string.lower():
                tomorrow = now + timedelta(days=1)
                if "pm" in time_string.lower():
                    hour = int(time_string.lower().split("at ")[1].split("pm")[0].strip())
                    return datetime(tomorrow.year, tomorrow.month, tomorrow.day, hour+12 if hour < 12 else hour)
                elif "am" in time_string.lower():
                    hour = int(time_string.lower().split("at ")[1].split("am")[0].strip())
                    return datetime(tomorrow.year, tomorrow.month, tomorrow.day, hour if hour < 12 else 0)
            
            # Simple format like "3pm today"
            if "today" in time_string.lower() and "pm" in time_string.lower():
                hour = int(time_string.lower().split("today")[0].strip().rstrip("pm"))
                return datetime(now.year, now.month, now.day, hour+12 if hour < 12 else hour)
            
            # Add more parsing logic here for different time formats
            
            # Default fallback - try to parse as exact datetime
            return datetime.strptime(time_string, "%Y-%m-%d %H:%M:%S")
            
        except Exception as e:
            print(f"Error parsing time: {e}")
            return None
    
        
