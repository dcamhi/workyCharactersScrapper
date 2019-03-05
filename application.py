# THIS IS THE FILE THAT CREATES THE FLASK APP

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

    # APP CONFIGURATIONS
    app.debug = debug
    app.testing = testing

    # DO NOT LOAD OLD FILES
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

    # SET DEFAULT PARSER - JSONPARSER
    app.config['DEFAULT_PARSERS'] = ['flask_api.parsers.JSONParser']

    # EXTRA CONFIGURATIONS
    app.config.update(config_overrides)
    charactersDB.init_app(app)

    # IMPORT BLUEPRINTS
    from characters.api import characters_app

    # REGISTER BLUEPRINTS
    app.register_blueprint(characters_app, url_prefix="/api/v1/")

    Compress(app)

    return app
