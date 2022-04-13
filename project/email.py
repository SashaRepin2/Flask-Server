import os
from threading import Thread

from flask import current_app, render_template
from flask_mail import Message
from project import mail
from config import Config


# def sendMessageToEmail(email, link):
#     # Отправка сообщения почту пользователя
#     msg = Message("Registration", recipients=[email])
#     msg_link = f'{app.config["SERVER_URL"]}/activate/{link}'
#     msg.html = '<div> ' \
#                '<h1>Для активации аккаунта перейдите на ссылке:</h1> ' \
#                f'<a href="{msg_link}">переход по ссылке</a>' \
#                '</div>'
#     mail.send(msg)


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
