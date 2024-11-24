import os
import sys
import subprocess

# Define the base folder for the data (you might need to adjust it to your actual directory structure)
base_folder = os.path.dirname(__file__)

# Define the paths to each of the scripts you want to run
scripts = [
    'data_process.py',
    'device_data_process.py',
    'geo_location_data_process.py',
    'peak_hours_data_process.py',
]

# Change the working directory to the base folder to ensure relative imports work (if needed)
os.chdir(base_folder)

# Run each script in sequence
for script in scripts:
    script_path = os.path.join(base_folder, script)
    if os.path.exists(script_path):
        print(f"Running {script}...")
        try:
            subprocess.run([sys.executable, script_path], check=True)
            print(f"{script} ran successfully!")
        except subprocess.CalledProcessError as e:
            print(f"Error running {script}: {e}")
    else:
        print(f"{script} not found in the specified path.")
