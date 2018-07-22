import os
from dotenv import load_dotenv

class Config:
  SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24)
  BASEDIR = os.path.abspath(os.path.dirname(__file__))
  SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(BASEDIR, 'app.db')
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  UPLOAD_FOLDER = BASEDIR + '/app/static/img/uploads'
  PORTFOLIO_FOLDER = BASEDIR + '/app/static/img/portfolio/uploads'
  POSTS_PER_PAGE = 5
  MAIL_SERVER = os.environ.get('MAIL_SERVER') or os.getenv('MAIL_SERVER')
  MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25) or os.getenv('MAIL_PORT')
  MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None or os.getenv('MAIL_USE_TLS')
  MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or os.getenv('MAIL_USERNAME')
  MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or os.getenv('MAIL_PASSWORD')
  SECURITY_EMAIL_SENDER = 'derekhawkins.tech@gmail.com'
  ADMINS = ['derekhawkins.tech@gmail.com', 'derekmhawkins@gmail.com']
  LOG_TO_STDOUT = os.environ.get('LOG_TO_STDOUT')
  S3_LOCATION = f"https://{os.getenv('S3_BUCKET')}.s3.amazonaws.com/"

load_dotenv(os.path.join(Config.BASEDIR, '.env'))
