import random
import string


# ANSI color escape codes for colorful printing
COLORS = {
    "RED": "\033[91m",
    "GREEN": "\033[92m",
    "YELLOW": "\033[93m",
    "BLUE": "\033[94m",
    "MAGENTA": "\033[95m",
    "CYAN": "\033[96m",
    "WHITE": "\033[97m",
    "RESET": "\033[0m"  # Reset to default color
}

class Password:
    def __init__(self, password):
        self.password = password

    def crack(self):
        attempts = 0  # Counter for attempts
        while True:  # Keep trying until the password is cracked
            guess = ''.join(random.choices(string.ascii_letters + string.digits, k=len(self.password)))  # Generate a random guess
            attempts += 1  # Increment attempts counter
            color = random.choice(list(COLORS.values())[:-1])  # Select a random color
            print(f"attempt # {attempts} - {color}{guess}{COLORS['RESET']}")  # Print the attempt in color
            if guess == self.password:  # Check if the guess matches the password
                return guess, attempts  # If so, return the cracked password and the number of attempts

class Username:
    def __init__(self, filename):
        self.usernames_passwords = self.load_usernames_passwords(filename)  # Load usernames and passwords from JSON file

    def load_usernames_passwords(self, filename):
        with open(filename, 'r') as file:
            data = json.load(file)  # Load JSON data from file
        return data

    def crack_password_for_username(self, username):
        if username in self.usernames_passwords:  # Check if the username exists
            password = Password(self.usernames_passwords[username])  # Get the password associated with the username
            print(f"Cracking password for {username}...")  # Print message indicating cracking has started
            cracked_password, attempts = password.crack()  # Crack the password
            print(f"The password for {username} is: {cracked_password} (cracked in {attempts} attempts).")  # Print the cracked password and number of attempts
        else:
            print("Username not found.")  # Print message if the username is not found

def main():
    username_manager = Username('db.json')  # Initialize Username class with the filename containing usernames and passwords
    username = input("Enter the username: ")  # Prompt user to enter username
    username_manager.crack_password_for_username(username)  # Call the method to crack the password for the provided username

if __name__ == "__main__":
    main()  # Execute the main function if this script is run directly
