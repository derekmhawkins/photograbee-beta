from flask import render_template
from flask_mail import Message
from app import app, mail
from app.forms import ContactForm

def send_email(subject, sender, recipients, text_body, html_body):
  msg = Message(subject, sender=sender, recipients=recipients)
  msg.body = text_body
  msg.html = html_body
  mail.send(msg)

def send_contact_form_email():
  context = {
    'recipient_name': "Shelby Cherie",
    'sender_name': ContactForm().name.data,
    'sender_email': ContactForm().email.data,
    'sender_message': ContactForm().body.data
  }
  send_email(
    '[Photograbee] You have an inquiry', 
    sender='noreply@photograbee.com', 
    recipients=[app.config['ADMINS'][:]],
    text_body=render_template('email/contact.txt', **context),
    html_body=render_template('email/contact.html', **context)
  )
