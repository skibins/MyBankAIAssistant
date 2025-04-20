from flask import Flask, render_template, request, redirect, url_for, session, flash, Blueprint, jsonify
from app.user import User
from app.gemini import GeminiAPI
from config import Config

# Initialize the blueprint
routes     = Blueprint('routes', __name__)
config     = Config()
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
    # Zwracamy już słownik z kluczami: chat_response, problem_title, problem_description
    return jsonify(ai_response)

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
    # Only allow logged-in users to access the assistant
    if 'user_email' not in session:
        return redirect(url_for('routes.index'))

    gemini_api.clear_history()
    return render_template('assistant.html')

@routes.route('/creditcards')
def creditcards():
    return render_template('services_subpages/creditcards.html')

@routes.route('/insurance')
def insurance():
    return render_template('services_subpages/insurance.html')

@routes.route('/investments')
def investments():
    return render_template('services_subpages/investments.html')

@routes.route('/loans')
def loans():
    return render_template('services_subpages/loans.html')

@routes.route('/savings')
def savings():
    return render_template('services_subpages/savings.html')

# Prevent caching of pages to ensure fresh authentication checks on back/forward navigation
@routes.after_request
def add_cache_control_headers(response):
    # Apply to all HTML responses
    content_type = response.headers.get('Content-Type', '')
    if content_type.startswith('text/html'):
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, private, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
    return response
