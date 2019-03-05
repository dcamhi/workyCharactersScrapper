#Configuration File
#IMPORT ALL VARIABLES FROM .env

import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

DEBUG_VAR = os.environ.get("DEBUG_VAR")
dbName = os.environ.get("dbName")
dbUrl = os.environ.get("dbUrl")

if DEBUG_VAR == 'True':
    DEBUG = "ON"
else:
    DEBUG = "FALSE"

# TIME ZONE VARIABLE
TIME_ZONE = os.environ.get("TIME_ZONE", "America/Mexico_City")
