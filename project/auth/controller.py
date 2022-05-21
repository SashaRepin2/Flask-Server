from flask import render_template, request, url_for, flash
from flask_login import current_user, login_user, logout_user
from werkzeug.utils import redirect

from .forms import RegistrationForm, LoginForm
from .. import db
from ..email import send_email
from ..models import User


def register():
    # If user already in account, then redirect him
    if current_user.is_authenticated:
        return redirect(url_for('main.all_blogs'))

    register_form = RegistrationForm()
    if register_form.validate_on_submit():
        # CREATE DB MODEL OBJECT
        user = User(
            first_name=register_form.first_name.data,
            last_name=register_form.last_name.data,
            login=register_form.login.data,
            email=register_form.email.data.lower(),
            password=register_form.password.data,
            gender=register_form.gender.data,
            confirmed_link='asd',
            age=True,
        )

        db.session.add(user)
        db.session.commit()

        # SEND MAIl TO USER
        # send_email(user.email, actLink=user.confirmed_link)

        flash('A confirmation email has been sent to you by email', 'auth')
        return redirect(url_for('auth.login'))

    return render_template('auth/registration.html', title='Register', form=register_form)


def login():
    # If user already in account, then redirect him
    if current_user.is_authenticated:
        return redirect(url_for('main.all_blogs'))

    # Validate form data
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data.lower()).first()
        login_user(user, True)
        return redirect(url_for('main.all_blogs', page=1))

    return render_template("auth/login.html", title='Login', form=login_form)


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
