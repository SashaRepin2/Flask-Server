# import logging.config
# import yaml
# logging.config.dictConfig(yaml.load(open('logging.conf'), Loader=yaml.Loader))  # Import logging config
from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate

from config import config
from flask_cors import CORS
# from flask_jwt_extended import JWTManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

# jwt = JWTManager()  # JWT system
db = SQLAlchemy()  # Database
mail = Mail()  # Mail
cors = CORS(supports_credentials=True)  # Create Cors
login_manager = LoginManager()


def create_app(config_name):
    app = Flask(__name__)  # Creating the server
    app.config.from_object(config[config_name])  # Loading the settings
    app.debug = True

    login_manager.init_app(app)
    # jwt.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    cors.init_app(app)

    # # Creates and registration blueprint
    # from project.api import api as api_blueprint
    # app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    from project.main import main as main_blueprint
    app.register_blueprint(main_blueprint)


    from project.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    # import main routes
    # from project.main import views

    return app
