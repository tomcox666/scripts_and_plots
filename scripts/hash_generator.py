import hashlib
from tkinter import filedialog
from tkinter import Tk
import os

def generate_hash(file_path, algorithm):
    if algorithm == 'MD5':
        hash_object = hashlib.md5()
    elif algorithm == 'SHA-256':
        hash_object = hashlib.sha256()
    else:
        raise ValueError('Invalid algorithm')

    with open(file_path, 'rb') as file:
        while True:
            chunk = file.read(4096)  # Read 4KB chunks
            if not chunk:
                break
            hash_object.update(chunk)

    return hash_object.hexdigest()

def verify_file_integrity(file_path, expected_hash, algorithm):
    actual_hash = generate_hash(file_path, algorithm)
    return actual_hash == expected_hash

def main():
    print("Welcome to the Hash Generator and File Integrity Verifier!")
    print("This program allows you to generate hashes for files and verify their integrity.")
    
    while True:
        print("\nMenu:")
        print("1. Generate hash for file")
        print("2. Verify file integrity")
        print("3. Exit")
        
        choice = input("Choose an option: ")
        
        if choice == '1':
            root = Tk()
            root.withdraw()  # Hiding the main window
            file_path = filedialog.askopenfilename(title="Select a file", initialdir=os.getcwd())
            
            if not file_path:
                print("No file selected. Please try again.")
                continue
            
            print("\nHash Algorithms:")
            print("1. MD5")
            print("2. SHA-256")
            
            algorithm_choice = input("Choose a hash algorithm: ")
            
            if algorithm_choice == '1':
                algorithm = 'MD5'
            elif algorithm_choice == '2':
                algorithm = 'SHA-256'
            else:
                print("Invalid choice. Please choose a valid algorithm.")
                continue
            
            try:
                hash_value = generate_hash(file_path, algorithm)
                print(f"The {algorithm} hash of the file is: {hash_value}")
            except FileNotFoundError:
                print("Error: The file was not found. Please check the file path and try again.")
            except ValueError as e:
                print(f"Error: {e}")
                
        elif choice == '2':
            root = Tk()
            root.withdraw()  # Hiding the main window
            file_path = filedialog.askopenfilename(title="Select a file", initialdir=os.getcwd())
            
            if not file_path:
                print("No file selected. Please try again.")
                continue
            
            expected_hash = input("Enter the expected hash: ")
            
            print("\nHash Algorithms:")
            print("1. MD5")
            print("2. SHA-256")
            
            algorithm_choice = input("Choose a hash algorithm: ")
            
            if algorithm_choice == '1':
                algorithm = 'MD5'
            elif algorithm_choice == '2':
                algorithm = 'SHA-256'
            else:
                print("Invalid choice. Please choose a valid algorithm.")
                continue
            
            try:
                if verify_file_integrity(file_path, expected_hash, algorithm):
                    print("The file integrity is verified.")
                else:
                    print("The file integrity is compromised.")
            except FileNotFoundError:
                print("Error: The file was not found. Please check the file path and try again.")
            except ValueError as e:
                print(f"Error: {e}")
                
        elif choice == '3':
            break
            
        else:
            print("Invalid choice. Please choose a valid option.")

if __name__ == "__main__":
    main()