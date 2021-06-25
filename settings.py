import os
from dotenv import load_dotenv
from pathlib import Path

files = list(Path(__file__).parent.glob('*.env'))
if files:
    load_dotenv(files[0])


class Configuration(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'abra-cadabra-ahalay-mohalay'
    DEBUG = True
    TESTING = False

    # sqlalchemy
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # flask babel
    LANGUAGES = ['en', 'ru']

    # flask security
    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT') or 'mysalt2strong'
    SECURITY_PASSWORD_HASH = "sha256_crypt"
    SECURITY_REGISTERABLE = True
    SECURITY_CONFIRMABLE = False
    SECURITY_RECOVERABLE = False
    SECURITY_SEND_REGISTER_EMAIL = False

    # Pagination
    POSTS_PER_PAGE = 10
    COMMENTS_PER_PAGE = 15

    # Logging
    PROJECT_LOGGING_FILE = True
    PROJECT_LOGGING_EMAIL = False
    LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')

    # mail
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or None
    MAIL_PORT = os.environ.get('MAIL_PORT') or None
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') or None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or None
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or None
    ADMINS = os.environ.get('ADMINS') or None
