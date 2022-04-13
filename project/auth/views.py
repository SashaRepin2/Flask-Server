# Осуществление регистрации пользователя
from flask import request, url_for
from flask_login import login_required, current_user
from werkzeug.utils import redirect

from project.auth import auth, controller


@auth.before_request
def before_request_main():
    if current_user.is_authenticated:
        if request.endpoint and request.blueprint != 'main' and request.endpoint not in ['static', 'auth.logout']:
            print(request.endpoint)
            return redirect(url_for('main.index', id=current_user.id))


@auth.route('/register', methods=['POST', 'GET'])
def register():
    return controller.register()


# Осуществление входа в аккаунт пользователя
@auth.route('/login', methods=['GET', 'POST'])
def login():
    return controller.login()


@auth.route('/logout', endpoint='logout')
@login_required
def logout():
    return controller.logout()


# Активация аккаунта пользователя через ссылку
@auth.route('/confirm/<link>')
def confirm(link):
    return controller.confirm(link)
