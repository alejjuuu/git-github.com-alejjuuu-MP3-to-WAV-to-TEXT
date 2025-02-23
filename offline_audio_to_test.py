import glob
import os
import speech_recognition as sr
import time
from pydub import AudioSegment
import re

def recognize_audio_with_timing(audio_file):
    start_time = time.time()
    
    with sr.AudioFile(audio_file) as source:
        print(f"Processing {audio_file}...")
        audio_data = recognizer.record(source)
    
    try:
        text = recognizer.recognize_sphinx(audio_data)
        end_time = time.time()
        print(f"Processed {audio_file} in {end_time - start_time:.2f} seconds")
        return text.strip()  # Strip any leading or trailing whitespace
    except sr.UnknownValueError:
        print(f"CMU Sphinx could not understand the audio in {audio_file}")
        return None
    except sr.RequestError:
        print("CMU Sphinx request error")
        return None


def save_transcription_to_file(filename, transcription, folder):
    # Save transcription without extra spaces or characters
    with open(os.path.join(folder, "transcriptions.txt"), "a") as file:
        file.write(transcription + "\n")  # Write each transcription on a new line


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


def natural_sort_key(s):
    # Split string into numbers and text, sort naturally
    return [int(text) if text.isdigit() else text.lower() for text in re.split('(\d+)', s)]


if __name__ == "__main__":
    recognizer = sr.Recognizer()  # Initialize before use

    folder_path = "../wav"
    output_folder = "chunks_output"
    
    # Create a folder for storing transcriptions
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Use glob to find all .wav files
    file_names = glob.glob(os.path.join(folder_path, "*.wav"))

    # Sort the files using a natural sort
    file_names.sort(key=lambda x: natural_sort_key(os.path.basename(x)))
    
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


'''
Break file into smaller chunks
pip install pydub

Ensure ffmpeg is installed as well (this is necessary for pydub to work with audio formats like .wav):
brew install ffmpeg



'''