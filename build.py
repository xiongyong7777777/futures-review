import os
import subprocess

# Install dependencies
subprocess.run(["pip", "install", "kivy", "matplotlib", "numpy", "sqlite3"])

# Run the app locally for testing
print("Running app locally...")
subprocess.run(["python", "main.py"])