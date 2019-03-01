"""This file is in charge of creating the Flask Application

On this file is defined all the Flask configurations such as SSL,
the compression of the static files and the main routes for the
API.
"""
from logging.config import dictConfig
from flask_api import FlaskAPI
from flask_compress import Compress
import config
import os
from flask_pymongo import PyMongo


charactersDB = PyMongo()

def create_app(debug: bool, testing: bool = False, **config_overrides) -> FlaskAPI:

    app = FlaskAPI(__name__, static_url_path='', static_folder='')

    app.config['MONGO_DBNAME'] = os.environ.get("dbName")
    app.config['MONGO_URI'] = os.environ.get("dbUrl")

    # Set current environment
    app.debug = debug
    app.testing = testing

    # Avoid loading old static files
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

    # Set parser directly to JSON
    app.config['DEFAULT_PARSERS'] = ['flask_api.parsers.JSONParser']

    # Set extra configurations
    app.config.update(config_overrides)
    charactersDB.init_app(app)

    # Import blueprints
    from characters.api import characters_app

    # Register blueprints
    app.register_blueprint(characters_app, url_prefix="/api/v1/")

    Compress(app)

    return app
