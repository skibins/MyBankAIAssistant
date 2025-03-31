from flask import Flask, render_template, request, redirect, url_for, session, flash, Blueprint, jsonify
from app.user import User
from app.gemini import GeminiAPI
import config
from config import Config

# Initialize the blueprint
routes = Blueprint('routes', __name__)
config = Config()
gemini_api = GeminiAPI(config)

@routes.route('/get_response', methods=['POST'])
def get_response():
    """
    Odbiera wiadomość użytkownika i zwraca odpowiedź z API Google Gemini.
    """
    data = request.get_json()
    user_input = data.get("message", "")

    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    ai_response = gemini_api.get_response(user_input)
    return jsonify({"response": ai_response})

@routes.route('/login', methods=['GET', 'POST'])
def login():
    # If the user is already logged in, redirect to the homepage
    if 'user_email' in session:
        return redirect(url_for('routes.index'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Load users from the JSON file
        users = User.load_data(config.DATA_FILE)['users']

        # Check if the login credentials are correct
        if User.authenticate(email, password, users):
            session['user_email'] = email
            return redirect(url_for('routes.index'))

        flash("Invalid email or password. Try again.", "error")
        return render_template('login.html', show_register_form=False)

    return render_template('login.html', show_register_form=False)


@routes.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirmPassword']

    # Load users from the JSON file
    users = User.load_data(config.DATA_FILE)['users']

    # Register the new user
    if not User.register(email, password, confirm_password, users, config.Config.DATA_FILE):
        return render_template('login.html', show_register_form=True)

    session['user_email'] = email
    return redirect(url_for('routes.index'))


@routes.route('/toggle_register')
def toggle_register():
    return render_template('login.html', show_register_form=True)


@routes.route('/toggle_login')
def toggle_login():
    return render_template('login.html', show_register_form=False)


@routes.route('/logout')
def logout():
    session.pop('user_email', None)
    return redirect(url_for('routes.index'))


@routes.route('/')
def index():
    return render_template('main.html')


@routes.route('/services')
def services():
    return render_template('services.html')


@routes.route('/about')
def about():
    return render_template('about.html')

@routes.route('/assistant')
def assistant():
    gemini_api.clear_history()
    return render_template('assistant.html')