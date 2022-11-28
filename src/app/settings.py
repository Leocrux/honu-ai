import os
from os.path import dirname, join

from dotenv import load_dotenv

dotenv_path = join(dirname(dirname(__file__)), ".env")
load_dotenv(dotenv_path)

SECRET_KEY = os.environ.get("SECRET_KEY")

MONGO_HOST = os.environ.get("MONGO_HOST")
MONGO_PORT = os.environ.get("MONGO_PORT")
MONGO_USER = os.environ.get("MONGO_INITDB_ROOT_USERNAME")
MONGO_PASSWORD = os.environ.get("MONGO_INITDB_ROOT_PASSWORD")
MONGO_DB = os.environ.get("MONGO_INITDB_DATABASE")

MONGO_DB_URL = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}"
