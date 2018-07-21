from app import app, db, mail
from app.models import User, Post, Category, Comment, Tag, Photo, Genre
from flask_mail import Message

@app.shell_context_processor
def make_shell_context():
  return {'db': db, 'User': User, 'Post': Post, 'Category': Category, 'Comment': Comment, 'Tag': Tag, 'Photo': Photo, 'Genre': Genre, 'Message': Message}
