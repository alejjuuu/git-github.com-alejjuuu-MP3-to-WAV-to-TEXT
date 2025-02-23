import os
import subprocess

# Specify the folder containing MP3 files
input_folder = '../convert_to_text/'
output_folder= '../convert_to_text/wav/'
# Check if the output folder exists, if not, create it
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Iterate over all MP3 files in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith('.mp3'):  # Check if the file is an MP3
        input_file = os.path.join(input_folder, filename)
        # Generate the output file path by changing the extension to .wav
        output_file = os.path.join(output_folder, f'{os.path.splitext(filename)[0]}.wav')

        # Run FFmpeg command to convert MP3 to WAV
        subprocess.run(['ffmpeg', '-i', input_file, output_file])

        print(f'Converted {filename} to {output_file}')