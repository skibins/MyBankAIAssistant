from flask import Flask, render_template, request, redirect, url_for, session, flash, Blueprint
from app.user import User
import config

# Initialize the blueprint
routes = Blueprint('routes', __name__)


@routes.route('/login', methods=['GET', 'POST'])
def login():
    # If the user is already logged in, redirect to the homepage
    if 'user_email' in session:
        return redirect(url_for('routes.index'))

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Load users from the JSON file
        users = User.load_data(config.Config.DATA_FILE)['users']

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
    users = User.load_data(config.Config.DATA_FILE)['users']

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
    return render_template('assistant.html')