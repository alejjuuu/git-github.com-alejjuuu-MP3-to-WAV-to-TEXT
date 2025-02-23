
# Habit Tracker Example
class HabitTracker:
    def __init__(self, habit_name):
        self.habit_name = habit_name
        self.streak = 0

    def track_day(self, completed=True):
        if completed:
            self.streak += 1
            print(f"Great! You’ve completed {self.habit_name}. Current streak: {self.streak} days.")
        else:
            self.streak = 0
            print(f"You missed today. Streak reset to {self.streak}.")


    # Habit Tracker Example
    habit = HabitTracker("Morning Exercise")
    habit.track_day(True)  # Complete habit
    habit.track_day(False)  # Miss habit