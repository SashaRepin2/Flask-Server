from flask import request, jsonify, url_for,
from werkzeug.utils import redirect

from project import db

from project.models import User

def auth_register():
        try:
            email = request.form['email']
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            login = request.form['login']
            age = request.form['age']
            gender = request.form['gender']
            agreement = request.form['agreement']
            password = request.form['password']

            # Check form, duplicate,
            # Add to db
            # Send email

            # if Users.get_user_by_email(email):
            #     return jsonify({'msg': "Users with such an email already exists"}), 409
            #
            # # Создание и добавление профиля пользователя
            # profile = Profile(form.username)
            # db.session.add(profile)
            # db.session.flush()
            #
            # # Создание и добавление токена пользователя
            # refresh_token = create_refresh_token(form.email)
            # ip_address = request.remote_addr
            # token = Token(ip_address=ip_address, refresh_token=refresh_token)
            # db.session.add(token)
            # db.session.flush()
            #
            # # Создание модели пользователя и добавление его в БД
            # user = Users(email=form.email, password=form.password,
            #             profile_id=profile.id,
            #             token_id=token.id)
            # db.session.add(user)
            # db.session.commit()

            # # Получение ссылки активации
            # activationLink = user.activationLink

            # sendMessageToEmail(email=user.email, link=activationLink)
            # send_email(to=user.email, actLink=activationLink)
            return jsonify({'msg': 'Registration success'}), 200

        except Exception as ex:
            print(ex)
            db.session.rollback()
            return ({"msg": "Internal Server Error"}), 500


def auth_login():
    if request.method == "POST":
        try:

            email = request.form['email']
            password = request.form['password']

            # Getting user
            user = User.get_user_with_email_and_password(email=email, password=password)

            if user is None:
                return jsonify({"msg": "Bad request or password"}), 400

            if not user.isActivated:
                return jsonify({"msg": 'Users account has not been activated. You need to activate your account!'})

            # Create new refresh and access tokens
            # access_token = create_access_token(identity=email)
            # refresh_token = create_refresh_token(identity=email)
            #
            # token = Token.query.filter(Token.id == user.token_id).first()
            # token.refresh_token = refresh_token
            # db.session.commit()

            # response = jsonify(
            #     {"msg": "Login completed successfully", "access_token": access_token})
            # response.set_cookie('access_token_cookie', access_token, samesite='None', httponly=True, secure=True)

            response = jsonify({"msg": 'success'})

            return response, 200

        except Exception as ex:
            return ({"msg": "Internal Server Error"}), 500

    return redirect(url_for('main.register'))
