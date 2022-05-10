from flask_login import login_required
from . import main
from . import controller


# import logging
# fileLogg = logging.getLogger('file')  # Logger for file
# consoleLogg = logging.getLogger('console')  # Logger for console

# @main.before_app_request
# def before_request_auth():
#     if current_user.is_anonymous:
#         if request.endpoint and request.blueprint != 'auth' and request.endpoint != 'static':
#             return redirect(url_for('auth.login'))
#
#
# @main.route("/", methods=["GET", "POST"])
# def redirect_to_page():
#     return redirect(url_for('main.all_blogs'))


# @main.route("/home", methods=["GET", "POST"])
# def home():
#     return controller.home()


@main.route("/profile/<int:id>", methods=["GET", "POST"])
@login_required
def profile(id):
    return controller.profile(id)


@main.route("/all-posts/<int:page>", methods=["GET", "POST"])
def all_blogs(page):
    return controller.all_blogs(page)


@main.route("/my-blogs/<int:page>", methods=["GET", "POST"])
def my_blogs(page):
    return 'myblogs ' + page


@main.route("/create-blog", methods=["GET", "POST"])
@login_required
def create_blog():
    return controller.create_blog()


@main.route("/upload/avatar", methods=["POST"])
@login_required
def upload_avatar():
    return controller.upload_avatar()


@main.route("/load/avatar/<int:id>", methods=["GET"])
@login_required
def load_avatar(id):
    return controller.load_avatar(id)
