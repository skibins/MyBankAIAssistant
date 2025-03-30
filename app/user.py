import json
from flask import flash

class User:
    def __init__(self, email, password, topics=None):
        self.email = email
        self.password = password
        self.topics = topics or []

    @staticmethod
    def load_data(data_file):
        """Load users from the JSON file."""
        with open(data_file, 'r', encoding='utf-8') as file:
            return json.load(file)

    @staticmethod
    def save_data(users, data_file):
        """Save users to the JSON file."""
        with open(data_file, 'w', encoding='utf-8') as file:
            json.dump({"users": users}, file, indent=4)

    @staticmethod
    def is_email_taken(email, users):
        """Check if the email already exists in the users list."""
        return any(user['email'] == email for user in users)

    @staticmethod
    def authenticate(email, password, users):
        """Authenticate the user based on email and password."""
        for user in users:
            if user['email'] == email and user['password'] == password:
                return True
        return False

    @staticmethod
    def register(email, password, confirm_password, users, data_file):
        """Register a new user."""
        if User.is_email_taken(email, users):
            flash("This email is already registered.", "error")
            return False

        if password != confirm_password:
            flash("Passwords do not match.", "error")
            return False

        new_user = {"email": email, "password": password, "topics": []}
        users.append(new_user)
        User.save_data(users, data_file)
        return True
