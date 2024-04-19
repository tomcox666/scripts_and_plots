import sqlite3
import hashlib
import binascii

def verify_password(stored_password, provided_password):
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', provided_password.encode('utf-8'), salt.encode('ascii'), 100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password

def get_password(username):
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    
    c.execute("SELECT password FROM passwords WHERE username = ?", (username,))
    stored_password = c.fetchone()[0]
    
    conn.close()
    
    return stored_password

def main():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    
    stored_password = get_password(username)
    
    if verify_password(stored_password, password):
        print("Password is correct!")
    else:
        print("Password is incorrect.")

if __name__ == "__main__":
    main()