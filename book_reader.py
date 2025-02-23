import nltk
from transformers import pipeline
from sumy.parsers.plaintext import PlaintextParser
from sumy.summarizers.lsa import LsaSummarizer
from datetime import datetime, timedelta

# Pre-process book text
nltk.download('punkt')

def load_book(file_path):
    """Load book text from a file"""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Summarization using BART (Transformers)
def summarize_using_bart(text, max_length=150, min_length=50):
    """Summarize the text using BART model"""
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    return summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)[0]['summary_text']

# Chunk the book into smaller sections
def chunk_text(text, chunk_size=1024):
    """Chunks the text into smaller sections"""
    return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

# Active recall testing
def test_recall(questions):
    """Simulates active recall by asking questions and checking answers"""
    print("Active Recall Test:\n")
    for question in questions:
        print(f"Question: {question}")
        input("Your answer (press Enter when done): ")
        print("Check if your answer is correct based on your notes or summary.\n")

# Spaced repetition system
def spaced_repetition(review_date):
    """Simulates a spaced repetition system by setting review dates"""
    next_review = datetime.now() + timedelta(days=review_date)
    print(f"Next review date: {next_review.strftime('%Y-%m-%d %H:%M:%S')}")
    return next_review

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

# Main function to process the book and summarize
def main():
    # Load the book content
    file_path = 'book.txt'  # Change this to the path of your book text file
    book_text = load_book(file_path)

    # Chunk the book into smaller sections for processing
    chunks = chunk_text(book_text)

    # Summarize each chunk using BART
    chunk_summaries = [summarize_using_bart(chunk) for chunk in chunks]

    # Combine all summaries into a final summary
    final_summary = "\n".join(chunk_summaries)

    # Print the final summary
    print("Final Book Summary:\n")
    print(final_summary)

    # Active recall (test yourself with questions)
    questions = ["What is the main takeaway from Chapter 1?", "How does habit stacking work?"]
    test_recall(questions)

    # Spaced repetition example
    review_intervals = [1, 3, 7, 14]
    for interval in review_intervals:
        spaced_repetition(interval)

    # Habit Tracker Example
    habit = HabitTracker("Morning Exercise")
    habit.track_day(True)  # Complete habit
    habit.track_day(False)  # Miss habit

if __name__ == "__main__":
    main()





#Make sure you have the required libraries installed:

#pip install spacy nltk transformers sumy

#python book_learning.py

