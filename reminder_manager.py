import schedule
import time
import datetime

class ReminderManager:
    def __init__(self):
        self.reminders = []

    def add_reminder(self, task):
        # Schedule reminder 5 minutes from now (for demo purposes)
        reminder_time = datetime.datetime.now() + datetime.timedelta(minutes=5)
        schedule.every().day.at(reminder_time.strftime("%H:%M")).do(self.notify, task)
        self.reminders.append({"task": task, "time": reminder_time.strftime("%H:%M")})
        print(f"Reminder scheduled for {task} at {reminder_time.strftime('%H:%M')}")

    def notify(self, task):
        print(f"Reminder: Time to {task}!")
        self.reminders = [r for r in self.reminders if r["task"] != task]  # Remove after notifying
        return schedule.CancelJob

    def start(self):
        while True:
            schedule.run_pending()
            time.sleep(1)

    def get_reminders(self):
        return self.reminders