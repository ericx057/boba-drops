import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
import time
import pygame

# Initialize pygame for audio
pygame.mixer.init()

class AlarmClock:
    def __init__(self, root):
        self.root = root
        self.root.title("Alarm Clock")
        self.root.geometry("300x250")

        self.alarm_time = None
        self.snooze_count = 0
        self.close_attempts = 0
        self.volume = 0.5  # Initial volume (50%)
        self.alarm_active = False  # Track if the alarm is currently active

        self.label = tk.Label(root, text="Set Alarm Time (HH:MM)", font=("Arial", 14))
        self.label.pack(pady=10)

        self.entry = tk.Entry(root, font=("Arial", 14))
        self.entry.pack(pady=10)

        self.set_button = tk.Button(root, text="Set Alarm", command=self.set_alarm)
        self.set_button.pack(pady=10)

        self.snooze_button = tk.Button(root, text="Snooze", command=self.snooze, state=tk.DISABLED)
        self.snooze_button.pack(pady=5)

        self.stop_button = tk.Button(root, text="Stop Alarm", command=self.stop_alarm, state=tk.DISABLED)
        self.stop_button.pack(pady=5)

        self.reset_button = tk.Button(root, text="Reset Alarm", command=self.reset_alarm, state=tk.DISABLED)
        self.reset_button.pack(pady=5)

    def set_alarm(self):
        alarm_time_str = self.entry.get()
        try:
            self.alarm_time = datetime.strptime(alarm_time_str, "%H:%M")
            self.label.config(text=f"Alarm set for {self.alarm_time.strftime('%H:%M')}")
            self.set_button.config(state=tk.DISABLED)  # Disable set button after setting alarm
            self.check_alarm()
            self.reset_button.config(state=tk.NORMAL)  # Enable reset button after alarm is set
        except ValueError:
            messagebox.showerror("Invalid Time", "Please enter time in HH:MM format")

    def check_alarm(self):
        now = datetime.now()
        if now >= self.alarm_time:
            self.trigger_alarm()
        else:
            self.root.after(1000, self.check_alarm)

    def trigger_alarm(self):
        self.alarm_active = True
        self.snooze_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.NORMAL)
        self.play_alarm()

    def play_alarm(self):
        pygame.mixer.music.load("alarm_sound.mp3")  # Replace with your alarm sound file
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play(-1)  # Loop the alarm sound

    def snooze(self):
        self.snooze_count += 1
        self.volume = min(1.0, self.volume + 0.1)  # Increase volume by 10%
        pygame.mixer.music.set_volume(self.volume)
        self.alarm_time += timedelta(minutes=5)  # Snooze for 5 minutes
        self.label.config(text=f"Snoozed! Alarm reset for {self.alarm_time.strftime('%H:%M')}")
        self.stop_alarm_timer()  # Stop any existing stop alarm timer
        self.check_alarm()  # Recheck alarm after 5 minutes

    def stop_alarm(self):
        self.close_attempts += 1
        if self.close_attempts >= 5:
            pygame.mixer.music.stop()
            self.play_final_audio()
            self.reset_alarm()
        else:
            self.label.config(text=f"Alarm will stop in 1 minute (Attempt {self.close_attempts}/5)")
            self.alarm_active = True
            self.root.after(60000, self.stop_alarm_timer)  # Wait 1 minute before stopping

    def stop_alarm_timer(self):
        if self.alarm_active:
            self.alarm_active = False
            pygame.mixer.music.stop()
            self.reset_alarm()

    def play_final_audio(self):
        pygame.mixer.music.load("final_audio.mp3")  # Replace with your final audio file
        pygame.mixer.music.play()

    def reset_alarm(self):
        self.snooze_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.DISABLED)
        self.reset_button.config(state=tk.DISABLED)  # Disable reset button when reset
        self.label.config(text="Set Alarm Time (HH:MM)")
        self.set_button.config(state=tk.NORMAL)  # Re-enable the set button after resetting
        self.entry.delete(0, tk.END)  # Optionally clear the entry field
        self.snooze_count = 0
        self.close_attempts = 0
        self.volume = 0.5
        self.alarm_active = False
        pygame.mixer.music.stop()  # Stop the alarm sound

if __name__ == "__main__":
    root = tk.Tk()
    app = AlarmClock(root)
    root.mainloop()
