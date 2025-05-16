import os

# === CHANGE THESE TO YOUR FOLDER PATHS ===
vision_dir = "/Users/athenamo/Documents/GitHub/SoundRT/Vision Files/VData/led/RTProcessing/"
sound_dir = "/Users/athenamo/Documents/GitHub/SoundRT/Sound Files/Data/Auditory-SRC/"
script_path = "/Users/athenamo/Documents/GitHub/SoundRT/Analysis Code/MeanAppend.py"
python_path = "/opt/anaconda3/bin/python"

# === Gather all CSV files in each directory ===
vision_files = {f.split('-')[0]: f for f in os.listdir(vision_dir) if f.endswith('.csv')}
sound_files = {f.split('-')[0]: f for f in os.listdir(sound_dir) if f.endswith('.csv')}

# === Match files by name prefix and format the output ===
matched_commands = []
for name in vision_files:
    if name in sound_files:
        vision_file_path = os.path.join(vision_dir, vision_files[name])
        sound_file_path = os.path.join(sound_dir, sound_files[name])
        matched_commands.append(f'"{vision_file_path},{sound_file_path}"')

# === Construct the final command line ===
if matched_commands:
    final_command = f'{python_path} "{script_path}" ' + ' '.join(matched_commands)
    print(final_command)
else:
    print("No matching files found.")
