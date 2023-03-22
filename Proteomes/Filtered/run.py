import os
import subprocess

THRESHOLD = 1.0e-10 # threshold value to set

folder_path = "../Annotated"
# iterate through all Annotated files and run filter
for filename in os.listdir(folder_path):
    filepath = os.path.join(folder_path, filename)
    subprocess.run(["python3", 'filter.py', str(THRESHOLD), filepath], capture_output=True, text=True)
