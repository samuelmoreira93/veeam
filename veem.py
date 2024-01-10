import os
import shutil
import time

def synchronize_folders(source_folder, replica_folder, interval, log_file):
    while True:
        # Synchronize folders
        for root, dirs, files in os.walk(source_folder):
            for file in files:
                origin = os.path.join(root, file)
                replica = os.path.join(replica_folder, os.path.relpath(root, source_folder), file)
                
                # Check if the file already exists in the replica folder
                if not os.path.isfile(replica):
                    # Copy the file to the mirror folder
                    shutil.copy2(origin, replica)
                    register_operation("Creation", replica, log_file)
        
        for root, dirs, files in os.walk(replica_folder):
            for file in files:
                original = os.path.join(source_folder, os.path.relpath(root, replica_folder), file)
                replica = os.path.join(root, file)
                
                # Check if the file no longer exists in the source folder
                if not os.path.isfile(original):
                    # Delete the file from the mirror folder
                    os.remove(replica)
                    register_operation("Elimination", replica, log_file)
        
        # Wait the specified time interval
        time.sleep(interval)

def register_operation(operation, file, log_file):
    with open(log_file, "a") as file:
        file.write(f"{operation}: {file.name}\n")
    print(f"Registered operation: {operation}: {file}")

# Prompt user for folder paths, sync interval and log file path
source_folder = input("Enter the path to the source folder: ")
replica_folder = input("Enter the path to the replica folder: ")
interval = int(input("Enter the synchronization interval in seconds: "))
log_file = input("Enter the path to the log file: ")

# Calling the folder synchronization function
synchronize_folders(source_folder, replica_folder, interval, log_file)