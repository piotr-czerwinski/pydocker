from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_babel import Babel
import sendgrid
from flask import request

app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'auth.login'
mail = sendgrid.SendGridAPIClient(apikey=app.config['SENDGRID_API_KEY'])
bootstrap = Bootstrap(app)
babel = Babel(app)
moment = Moment(app)

from web import models

from web.main import bp as main_bp
app.register_blueprint(main_bp)

from web.models import User

from web.errors import bp as errors_bp
app.register_blueprint(errors_bp)

from web.auth import bp as auth_bp
app.register_blueprint(auth_bp, url_prefix='/auth')

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

import logging
from logging.handlers import RotatingFileHandler
import os

if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/pydocker.log', maxBytes=10240,
                                       backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Microblog startup')


@babel.localeselector
def get_locale():
    return request.accept_languages.best