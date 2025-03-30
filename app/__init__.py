from flask import Flask
from app.routes import routes

def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config.from_object('config.Config')  # Load config from config.py

    # Register the Blueprint
    app.register_blueprint(routes)

    return app
