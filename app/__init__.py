import logging
import os
import sys

from flask import Flask
from dotenv import load_dotenv

load_dotenv()

DEBUG = os.getenv("DEBUG", False)


def create_app():
    flask = Flask(__name__)
    flask.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024
    flask.config["PHRASEFILE_EXTENSIONS"] = {".txt"}
    flask.config["SOUNDFILE_EXTENSIONS"] = {".wav"}
    flask.config["DEBUG"] = DEBUG
    return flask


logging_settings = dict(
    filename="flask.log",
    level=logging.WARN,
    format="%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s",
)
if DEBUG:
    # in debugging (local dev) mode, send logs to standard output
    del logging_settings["filename"]
    logging_settings["stream"] = sys.stdout

logging.basicConfig(**logging_settings)

app = create_app()
