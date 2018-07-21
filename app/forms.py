from flask_wtf import FlaskForm
from wtforms import FileField, StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, SelectMultipleField, widgets
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import User, Tag
from flask import request

class LoginForm(FlaskForm):
  email = StringField('Email', validators=[DataRequired()])
  password = PasswordField('Password', validators=[DataRequired()])
  remember_me = BooleanField('Remember Me')
  submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
  name = StringField('Name', validators=[DataRequired()])
  email = StringField('Email', validators=[DataRequired()])
  password = PasswordField('Password', validators=[DataRequired()])
  password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
  submit = SubmitField('Register')

  def validate_email(self, email):
    user = User.query.filter_by(email=email.data).first()
    if user is not None:
      raise ValidationError('Please use a different email.')


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class BlogForm(FlaskForm):
  name = StringField('Name', validators=[DataRequired()])
  title = StringField('Title', validators=[DataRequired()])
  image = FileField('Upload a Photo', validators=[DataRequired()])
  body = TextAreaField('Blog Post', validators=[DataRequired()])
  category = SelectField('Categories', coerce=int, choices=[])
  tags = StringField('Tags')
  submit = SubmitField('Post')


class CategoryForm(FlaskForm):
  name = StringField('Category Name', validators=[DataRequired()])
  submitCategory = SubmitField('Add Category') 


class CommentForm(FlaskForm):
  name = StringField('Your Name *', validators=[DataRequired()])
  body = TextAreaField('Your Comment...', validators=[DataRequired()])
  submit = SubmitField('Post Comment')


class PortfolioForm(FlaskForm):
  model_name = StringField('Name of model', validators=[DataRequired()])
  image = FileField('Upload photo', validators=[DataRequired()])
  event = StringField('Name of event', validators=[DataRequired()])
  synopsis = TextAreaField('Write a synopsis...', validators=[DataRequired()])
  camera = StringField('Type of camera', validators=[DataRequired()])
  lens = StringField('Type of lens', validators=[DataRequired()])
  focus = StringField('Focus', validators=[DataRequired()])
  shutter = StringField('Shutter', validators=[DataRequired()])
  iso = StringField('ISO', validators=[DataRequired()])
  genre = SelectField('Select a genre', coerce=int, choices=[])
  submitPhoto = SubmitField('Add Photo')


class ContactForm(FlaskForm):
  name = StringField('Your Name', validators=[DataRequired()])
  email = StringField('Your E-mail', validators=[DataRequired()])
  body = TextAreaField('Your Message...', validators=[DataRequired()])
  submit = SubmitField('Send Message')