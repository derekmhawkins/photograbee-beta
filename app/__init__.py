from flask import Flask
from flask_bootstrap import Bootstrap
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment
from flask_mail import Mail
import logging
from logging.handlers import SMTPHandler

app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
moment = Moment(app)
mail = Mail(app)

if not app.debug:
  if app.config['MAIL_SERVER']:
    auth = None
    if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
      auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSSWORD'])
      secure = None
      if app.config['MAIL_USE_TLS']:
        secure = ()
      mail_handler = SMTPHandler(
        mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
        fromaddr='no-reply@' + app.config['MAIL_SERVER'],
        toaddrs=app.config['ADMINS'], subject='Photograbee Failure',
        credentials=auth, secure=secure)
      mail_handler.setLevel(logging.ERROR)
      app.logger.addHandler(mail_handler)

# def create_app(config_class=Config):
#   app = Flask(__name__)
#   app.config.from_object(config_class)
#   if not app.debug:
#     if app.config['LOG_TO_STDOUT']:
#       stream_handler = logging.StreamHandler()
#       stream_handler.setLevel(logging.INFO)
#       app.logger.addHandler(stream_handler)
#     else:
#       if not os.path.exists('logs'):
#         os.mkir('logs')
#       file_handler = RotatingFileHandler('logs/main.log', maxBytes=10240, backupCount=10)
#       file_handler.setFormatter(logging.Formatter('{asctime} {levelname}: {message} [in {pathname}: {lineno}]'))
#       file_handler.setLevel(logging.INFO)
#       app.logger.addHandler(file_handler)
    
#     app.logger.setLevel(logging.INFO)
#     app.logger.info('Microblog startup')
  
#   return app

from app import routes, models