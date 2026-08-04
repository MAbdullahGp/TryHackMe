import os
import subprocess
import sys

# Open the dictionary file safely
with open("random.dic", "r") as f:
    for line in f:
        # Remove trailing newline characters and spaces
        key = line.strip()
        
        # Skip empty lines
        if not key:
            continue
            
        print(f"Trying: {key}")
        
        # Run the program with the key as an argument
        result = subprocess.run(["./program", key], capture_output=True, text=True)
        
      
           print(f"Output: {result.stdout.strip()}")
            
      # Check if it succeeded (adjust condition based on exit code or output)
     if result.returncode == 0:
            print(f"\n[+] Found correct password: {key}\n")
