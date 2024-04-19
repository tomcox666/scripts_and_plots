import string
import secrets
import sqlite3
import hashlib
import binascii
import os

def generate_password(length, use_uppercase, use_numbers, use_special_chars):
    characters = string.ascii_lowercase
    
    if use_uppercase:
        characters += string.ascii_uppercase
    if use_numbers:
        characters += string.digits
    if use_special_chars:
        characters += string.punctuation
    
    return ''.join(secrets.choice(characters) for _ in range(length))

def hash_password(password):
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')

def store_password(password, username):
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS passwords
                 (username text, password text)''')
    
    c.execute("INSERT INTO passwords VALUES (?, ?)", (username, hash_password(password)))
    
    conn.commit()
    conn.close()

def main():
    length = int(input("Enter the desired password length: "))
    
    use_uppercase = input("Include uppercase letters? (yes/no/y/n): ").lower() in ['yes', 'y']
    use_numbers = input("Include numbers? (yes/no/y/n): ").lower() in ['yes', 'y']
    use_special_chars = input("Include special characters? (yes/no/y/n): ").lower() in ['yes', 'y']
    
    password = generate_password(length, use_uppercase, use_numbers, use_special_chars)
    
    print(f"Generated Password : {password}")
    
    happy = input("Are you happy with this password? (yes/no/y/n): ").lower() in ['yes', 'y']
    
    if happy:
        username = input("Enter a username to store the password under: ")
        store_password(password, username)
        print("Password stored successfully!")
    else:
        print("Password not stored. Please run the program again to generate a new password.")

if __name__ == "__main__":
    main()