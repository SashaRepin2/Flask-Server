import os
from threading import Thread

from flask import current_app, render_template
from flask_mail import Message
from project import mail
from config import Config


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, actLink):
    app = current_app._get_current_object()
    to = 'sasharepin2016@gmail.com'
    msg = Message("Registration", recipients=[to])
    msg.html = render_template("email/message.html", link=actLink)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr
