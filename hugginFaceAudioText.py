import os
import glob
import time
import re
import nltk
import torch
import whisper
from pydub import AudioSegment
import speech_recognition as sr
from transformers import pipeline
from datetime import datetime, timedelta
from nltk.tokenize import sent_tokenize

# Disable tokenizer parallelism warning
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Download necessary NLTK data
nltk.download('punkt')

# Initialize the Whisper model for transcription
whisper_model = whisper.load_model("base")

# Initialize the CMU Sphinx recognizer
recognizer = sr.Recognizer()

# Convert audio file to WAV format
def convert_to_wav(audio_file_path):
    audio = AudioSegment.from_file(audio_file_path)
    wav_path = audio_file_path.rsplit(".", 1)[0] + ".wav"
    audio.export(wav_path, format="wav")
    return wav_path

# Load book content from a file
def load_book(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

# Summarization using BART (Transformers)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_using_bart(text, max_length=150, min_length=50):
    try:
        return summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)[0]['summary_text']
    except Exception as e:
        print(f"Summarization error: {e}")
        return text

# Chunk the book into smaller sections
def chunk_text(text, max_chunk_size=1024):
    sentences = sent_tokenize(text)
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) <= max_chunk_size:
            current_chunk += sentence + " "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + " "

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks

# Active recall testing
def test_recall(questions, output_filename="recall_test.txt"):
    """Simulates active recall by asking questions and saving answers to a file"""
    with open(output_filename, "w", encoding="utf-8") as file:
        file.write("Active Recall Test:\n\n")
        for question in questions:
            file.write(f"Question: {question}\n")
            answer = input("Your answer (press Enter when done): ")
            file.write(f"Your Answer: {answer}\n")
            file.write("Check if your answer is correct based on your notes or summary.\n\n")
    print(f"Active recall test saved to {output_filename}")

# Spaced repetition system
def spaced_repetition(review_date):
    next_review = datetime.now() + timedelta(days=review_date)
    print(f"Next review date: {next_review.strftime('%Y-%m-%d %H:%M:%S')}")
    return next_review

# Transcribe audio using Whisper
def transcribe_audio(audio_file_path):
    try:
        audio = whisper.load_audio(audio_file_path)  # Load using Whisper's optimized function
        audio = whisper.pad_or_trim(audio)  # Ensure the length is manageable
        result = whisper_model.transcribe(audio)
        return result['text']
    except Exception as e:
        print(f"Error in transcription: {e}")
        return ""



def recognize_audio_with_timing(audio_file):
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)

    try:
        # Try CMU Sphinx first
        return recognizer.recognize_sphinx(audio_data).strip()
    except (sr.UnknownValueError, sr.RequestError):
        print(f"CMU Sphinx failed for {audio_file}, switching to Whisper...")

        try:
            # Use Whisper as a backup
            audio = whisper.load_audio(audio_file)
            audio = whisper.pad_or_trim(audio)
            result = whisper_model.transcribe(audio)
            return result['text']
        except Exception as e:
            print(f"Whisper also failed for {audio_file}: {e}")
            return None




# Save transcription to a file
def save_transcription_to_file(filename, transcription, folder):
    with open(os.path.join(folder, "transcriptions.txt"), "a") as file:
        file.write(transcription + "\n")  # Write each transcription on a new line

# Split audio into chunks
def split_audio_into_chunks(audio_file, chunk_length_ms=30000):
    audio = AudioSegment.from_wav(audio_file)  # Load audio
    audio_length = len(audio)
    chunks = []

    # Create a folder for saving chunks if it doesn't exist
    chunk_folder = os.path.join(os.path.dirname(audio_file), "chunks")
    if not os.path.exists(chunk_folder):
        os.makedirs(chunk_folder)

    for start_ms in range(0, audio_length, chunk_length_ms):
        chunk = audio[start_ms:start_ms + chunk_length_ms]
        chunk_filename = f"{os.path.basename(audio_file).split('.')[0]}_chunk_{start_ms // 1000}.wav"
        chunk_path = os.path.join(chunk_folder, chunk_filename)  # Save chunk in the new folder
        chunk.export(chunk_path, format="wav")
        chunks.append(chunk_path)

    return chunks

# Natural sort for file names
def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split('(\d+)', s)]

# Function to save output to a file
def save_output(filename, content):
    with open(filename, "w", encoding="utf-8") as file:
        file.write(content)



def main():
    folder_path = "/Users/alejandro/Desktop/Docker/wav/chunks/"  # Your folder with .wav files
    output_folder = "chunks_output"

    # Create a folder for storing transcriptions
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Use glob to find all .wav files
    file_names = glob.glob(os.path.join(folder_path, "*.wav"))

    print(file_names)
    
    # Sort the files using a natural sort
    file_names.sort(key=lambda x: natural_sort_key(os.path.basename(x)))

    # Process each audio file
    for filename in file_names:
        print(f"Processing file {filename}...")

        # Split the audio into smaller chunks
        chunks = split_audio_into_chunks(filename)

        # Transcribe each chunk and save it to the file
        for chunk in chunks:
            transcription = recognize_audio_with_timing(chunk)
            if transcription:
                save_transcription_to_file(chunk, transcription, output_folder)
            else:
                print(f"Failed to transcribe {chunk}")

    # Load the entire transcribed text
    file_path = '/Users/alejandro/Desktop/Docker/Main_Python/chunks_output/transcriptions.txt'
    book_text = load_book(file_path)



    # Summarize all the text at once
    final_summary = summarize_using_bart(book_text, max_length=500, min_length=200)

    # Print and save final summary
    #print("Final Summary:\n", final_summary)
    save_output("transcribed_text.txt", final_summary)

if __name__ == "__main__":
    main()

