from flask import request, url_for
from flask_login import login_required, current_user
from werkzeug.utils import redirect

from . import main
from . import controller


# import logging
# fileLogg = logging.getLogger('file')  # Logger for file
# consoleLogg = logging.getLogger('console')  # Logger for console


@main.before_app_request
def before_request_auth():
    if current_user.is_anonymous:
        if request.endpoint and request.blueprint != 'auth' and request.endpoint != 'static':
            return redirect(url_for('auth.login'))


@main.route("/", methods=["GET", "POST"])
def home_page():
    return redirect(url_for('auth.login'))


@main.route("/profile/<int:id>", methods=["GET", "POST"])
@login_required
def index(id):
    return controller.index(id)


@main.route("/all-posts/<int:page>", methods=["GET", "POST"])
@login_required
def all_posts(page):
    return controller.all_posts(page)


@main.route("/create-post", methods=["GET", "POST"])
@login_required
def create_post():
    return controller.create_post()

# @main.route("/users", methods=["GET", "POST"])
# @jwt_required()
# def get_all_users():
#     users = Users.query.all()
#     result = []
#
#     for user in users:
#         result.append(user.email)
#
#     return jsonify({"users": result, "count_users": len(result)}), 200
#
#
# @main.route("/cookies", methods=["GET"])
# def get_cookies():
#     response = make_response("Here, take some cookie!")
#     access_token = create_access_token(identity="admin")
#     response.set_cookie('access_token_cookie', access_token, samesite='None', httponly=True, secure=True)
#     return response
#
#
# @main.route("/check-cookies", methods=["GET"])
# @jwt_required()
# def get_check_cookies():
#     print(request.cookies.get('access_token'))
#     username = get_jwt_identity()
#     response = make_response("Here, give me some cookie!")
#
#     response.delete_cookie('access_token_cookie', samesite='None', httponly=True, secure=True)
#     print(username)
#     return response


# @main.route('/', methods=['GET', 'POST'])
# @login_required
# def posts():
#     return controller.posts()
