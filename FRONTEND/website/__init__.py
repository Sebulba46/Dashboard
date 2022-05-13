from flask import Flask
from flask import send_from_directory, redirect, url_for, request


def create_app():
    app = Flask(__name__, static_folder='static')
    app.config['SECRET_KEY'] = 'sdklsdj'

    from .auth import auth

    app.register_blueprint(auth, url_refix='/')

    return app
