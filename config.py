import datetime
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'


    APP_NAME = os.environ.get('APP_NAME') or 'Flask app'
    FLASK_RUN_HOST = 'localhostd'
    SERVER_URL = os.environ.get('SERVER_URL') or 'http://localhost:5000'
    CLIENT_URL = os.environ.get('CLIENT_URL') or 'http://yandex.ru'

    # FLASK_APP

    # CORS CONFIG
    # CORS_ORIGINS = "http://localhost:3000"

    # MAIL CONFIGS
    MAIL_SERVER = os.environ.get('MAIL_SERVER', "smtp.gmail.com")
    MAIL_PORT = os.environ.get('MAIL_PORT', '587')
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_USE_TLS = True
    MAIL_DEBUG = False

    # SQLALCHEMY CONFIGS
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT CONFIGS
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_TOKEN_LOCATION = 'cookies'

    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(minutes=5)
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=2)
    JWT_COOKIE_CSRF_PROTECT = False

    # WTF_CSRF_ENABLED = False


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
    JWT_COOKIE_CSRF_PROTECT = True


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}
