import os
from dotenv import load_dotenv
from pathlib import Path

file = list(Path(__file__).parent.glob('*.env'))[0]
load_dotenv(file)


class Configuration(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'abra-cadabra-ahalay-mohalay'
    print(SECRET_KEY)
    DEBUG = True
    TESTING = False

    # sqlalchemy
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or 'sqlite:///'
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
    POSTS_PER_PAGE = 3
    COMMENTS_PER_PAGE = 5

    # Logging
    PROJECT_LOGGING_FILE = True
    PROJECT_LOGGING_EMAIL = False

    # mail
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = os.environ.get('MAIL_PORT')
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = os.environ.get('ADMINS')
