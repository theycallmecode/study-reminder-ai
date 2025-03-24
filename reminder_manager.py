import schedule
import time
import datetime

class ReminderManager:
    def __init__(self):
        self.reminders = []

    def add_reminder(self, task):
        # Default: 5 minutes from now
        reminder_time = datetime.datetime.now() + datetime.timedelta(minutes=5)
        self._schedule_task(task, reminder_time)

    def add_reminder_with_time(self, task, time_str):
        # Parse specific time (e.g., "14:30")
        now = datetime.datetime.now()
        reminder_time = datetime.datetime.strptime(f"{now.date()} {time_str}", "%Y-%m-%d %H:%M")
        if reminder_time < now:
            reminder_time += datetime.timedelta(days=1)  # Move to next day if time has passed
        self._schedule_task(task, reminder_time)

    def _schedule_task(self, task, reminder_time):
        schedule.every().day.at(reminder_time.strftime("%H:%M")).do(self.notify, task)
        self.reminders.append({"task": task, "time": reminder_time.strftime("%H:%M")})
        print(f"Reminder scheduled for '{task}' at {reminder_time.strftime('%H:%M')}")

    def notify(self, task):
        print(f"Reminder: Time to '{task}'!")
        self.reminders = [r for r in self.reminders if r["task"] != task]
        return schedule.CancelJob

    def start(self):
        while True:
            schedule.run_pending()
            time.sleep(1)

    def get_reminders(self):
        return self.reminders