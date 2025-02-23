import speech_recognition as sr
import os
import time

# Initialize recognizer
recognizer = sr.Recognizer()

# Path to the folder
folder_path = '../wav/'

# List to store the filenames
file_names = []

# Iterate through the folder and get the file names
for filename in os.listdir(folder_path):
    # Check if it's a file (not a directory)
    if os.path.isfile(os.path.join(folder_path, filename)):
        file_names.append(filename)




def recognize_audio(audio_file):
    with sr.AudioFile(audio_file) as source:
        print(f"Processing {audio_file}...")
        audio_data = recognizer.record(source)

    try:
        # Use CMU Sphinx for offline recognition
        text = recognizer.recognize_sphinx(audio_data)
        return text
    except sr.UnknownValueError:
        print(f"CMU Sphinx could not understand the audio in {audio_file}")
        return None
    except sr.RequestError:
        print("CMU Sphinx request error")
        return None



def recognize_audio1(audio_file, retries=3):
    for attempt in range(retries):
        try:
            with sr.AudioFile(audio_file) as source:
                print(f"Processing {audio_file}...")
                audio_data = recognizer.record(source)

            # Use Google Web Speech API (requires internet connection)
            text = recognizer.recognize_google(audio_data)
            return text  # If successful, return the transcription

        except sr.UnknownValueError:
            print(f"Google Speech Recognition could not understand the audio in {audio_file}")
            return None
        except sr.RequestError:
            print("Could not request results from Google Speech Recognition service")
            if attempt < retries - 1:
                print("Retrying...")
                time.sleep(2)  # Wait before retrying
            else:
                print("Max retries reached. Skipping this file.")
                return None

for filename in file_names:
    audio_file = os.path.join(folder_path, filename)
    transcription = recognize_audio(audio_file)
    if transcription:
        print("Transcription: ", transcription)
    else:
        print(f"Failed to transcribe {filename}")




#pip install pocketsphinx
