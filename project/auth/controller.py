from flask import render_template, request, url_for, flash
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.utils import redirect

from .forms import RegistrationForm, LoginForm
from .. import db
from ..email import send_email
from ..models import User


def register():
    registerForm = RegistrationForm()
    if registerForm.validate_on_submit():
        user = User(
            first_name=registerForm.first_name.data,
            last_name=registerForm.last_name.data,
            login=registerForm.login.data,
            email=registerForm.email.data.lower(),
            password=registerForm.password.data,
            gender=registerForm.gender.data,
            age=True,
        )

        db.session.add(user)
        db.session.commit()
        send_email(user.email, actLink=user.activationLink)
        flash('A confirmation email has been sent to you by email', 'auth')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', title='Register', form=registerForm)


def login():
    loginForm = LoginForm()
    if loginForm.validate_on_submit():

        # If user already in account
        if current_user.is_authenticated:
            redirect(url_for('main.index'))

        user = User.query.filter_by(email=loginForm.email.data).first()

        if user is not None and user.verify_password(loginForm.password.data):
            login_user(user, loginForm.remember.data)
            return redirect(url_for('main.index', id=user.id))

        flash('Invalid username or password', 'auth')

    return render_template("auth/login.html", title='Login', form=loginForm)


def logout():
    logout_user()
    return redirect(url_for('auth.login'))


def confirm(link):
    # Поиск пользователя с данной ссылкой
    user = User.get_user_by_activation_link(link)
    if user is None or user.isActivated:
        flash("Current activation link is not valid", 'email')
    else:
        # Актвируем аккаунт
        user.isActivated = True
        db.session.commit()
        flash('You success confrim your email', 'email')

    return render_template('auth/confirm.html', title='Confirm email')

    # fileLogg.info(f"Users with email: {user.email} has been activated")
    # response = make_response(redirect(current_app.config.get("CLIENT_URL"), code=302))

    # except Exception as ex:
    #     return ({"msg": "Internal Server Error"}), 500
