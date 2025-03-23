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