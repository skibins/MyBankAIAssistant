from flask import Flask, render_template, request, redirect, url_for, session, flash, Blueprint, jsonify
from app.user import User
from app.gemini import GeminiAPI
from config import Config

# Initialize the Routes blueprint
routes     = Blueprint('routes', __name__)
config     = Config()
gemini_api = GeminiAPI(config)

@routes.route('/get_response', methods=['POST'])
def get_response():
    """
    Receives a message from the user and returns a response via the Google Gemini API.
    """
    data = request.get_json()
    user_input = data.get("message", "")

    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    ai_response = gemini_api.get_response(user_input)
    # Return a dictionary with keys: chat_response, problem_title, problem_description
    return jsonify(ai_response)

@routes.route('/login', methods=['GET', 'POST'])
def login():
    # Redirect already logged-in users to the homepage
    if 'user_email' in session:
        return redirect(url_for('routes.index'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Load user data from the JSON file
        users = User.load_data(config.DATA_FILE)['users']

        # Authenticate credentials
        if User.authenticate(email, password, users):
            session['user_email'] = email
            return redirect(url_for('routes.index'))

        flash("Invalid email or password. Try again.", "error")
        return render_template('login.html', show_register_form=False)

    # Show login form
    return render_template('login.html', show_register_form=False)

@routes.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirmPassword']

    # Load existing users
    users = User.load_data(config.DATA_FILE)['users']

    # Attempt to register new user
    if not User.register(email, password, confirm_password, users, config.Config.DATA_FILE):
        return render_template('login.html', show_register_form=True)

    session['user_email'] = email
    return redirect(url_for('routes.index'))

@routes.route('/toggle_register')
def toggle_register():
    # Show registration form toggle
    return render_template('login.html', show_register_form=True)

@routes.route('/toggle_login')
def toggle_login():
    # Show login form toggle
    return render_template('login.html', show_register_form=False)

@routes.route('/logout')
def logout():
    # Clear the user session and redirect to homepage
    session.pop('user_email', None)
    return redirect(url_for('routes.index'))

@routes.route('/')
def index():
    # Render the main landing page
    return render_template('main.html')

@routes.route('/services')
def services():
    # Render the services overview page
    return render_template('services.html')

@routes.route('/about')
def about():
    # Render the about page
    return render_template('about.html')

@routes.route('/assistant')
def assistant():
    # Restrict access to authenticated users
    if 'user_email' not in session:
        return redirect(url_for('routes.index'))

    # Reset chat history and render assistant interface
    gemini_api.clear_history()
    return render_template('assistant.html')

@routes.route('/creditcards')
def creditcards():
    # Render the Credit Cards service page
    return render_template('services_subpages/creditcards.html')

@routes.route('/insurance')
def insurance():
    # Render the Insurance service page
    return render_template('services_subpages/insurance.html')

@routes.route('/investments')
def investments():
    # Render the Investments service page
    return render_template('services_subpages/investments.html')

@routes.route('/loans')
def loans():
    # Render the Loans service page
    return render_template('services_subpages/loans.html')

@routes.route('/savings')
def savings():
    # Render the Savings service page
    return render_template('services_subpages/savings.html')

# Prevent caching of HTML pages to enforce fresh authentication on navigation
@routes.after_request
def add_cache_control_headers(response):
    content_type = response.headers.get('Content-Type', '')
    if content_type.startswith('text/html'):
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, private, max-age=0'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
    return response
