from app import db, login
from datetime import datetime
import re
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_login import UserMixin


post_tags = db.Table('post_tags',
  db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
  db.Column('post_id', db.Integer, db.ForeignKey('post.id'))
)

class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(100), unique=True)
  name = db.Column(db.String(50))
  password_hash = db.Column(db.String(128))
  posts = db.relationship('Post', backref='author', lazy='dynamic')
  is_admin = db.Column(db.Boolean, nullable=False, default=False)

  def __repr__(self):
    return "<User: {} | {}>".format(self.email, self.name)

  def set_password(self, password):
    self.password_hash = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.password_hash, password)


class Post(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(100))
  image = db.Column(db.String(255), nullable=True)
  body = db.Column(db.Text)
  created_on = db.Column(db.DateTime, index=True, default=datetime.utcnow)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
  comments = db.relationship('Comment', backref='comment', lazy='dynamic')
  tags = db.relationship('Tag', secondary=post_tags, backref=db.backref('posts', lazy='dynamic'))

  def __repr__(self):
    return "<Post: {}>".format(self.body)


class Category(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(64))
  posts = db.relationship('Post', backref='cat', lazy='dynamic')

  def __repr__(self):
    return "<Category: {}>".format(self.name)


class Comment(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50))
  body = db.Column(db.Text)
  created_on = db.Column(db.DateTime, index=True, default=datetime.utcnow)
  post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

  def __repr__(self):
    return "<Comment: {}>".format(self.body)

  
class Tag(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(10), nullable=True)

  def __repr__(self):
    return '<Tag: {}>'.format(self.name)


class Genre(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(50))
  photos = db.relationship('Photo', backref='genre', lazy='dynamic')

  def __repr__(self):
    return '<Genre: {}>'.format(self.name)


class Photo(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  model_name = db.Column(db.String(100))
  image = db.Column(db.String(100))
  event = db.Column(db.String(100))
  synopsis = db.Column(db.Text)
  camera = db.Column(db.String(50))
  lens = db.Column(db.String(50))
  focus = db.Column(db.String(50))
  shutter = db.Column(db.String(50))
  iso = db.Column(db.Integer)
  genre_id = db.Column(db.Integer, db.ForeignKey('genre.id'))
  timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

  def __repr__(self):
    return '<Photo: {} | {}>'.format(self.model_name, self.event)


@login.user_loader
def load_user(id):
  return User.query.get(int(id))
