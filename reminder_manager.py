import schedule
import time
import pyttsx3

# Initialize text-to-speech engine
engine = pyttsx3.init()

def speak_reminder(task):
    engine.say(f"Reminder: Time to {task}!")
    engine.runAndWait()

def schedule_reminder(time_str, task):
    # Schedule a reminder at the given time (e.g., "14:30")
    schedule.every().day.at(time_str).do(speak_reminder, task=task)
    print(f"Scheduled reminder: {task} at {time_str}")

def run_scheduler():
    # Keep the scheduler running in the background
    while True:
        schedule.run_pending()
        time.sleep(1)