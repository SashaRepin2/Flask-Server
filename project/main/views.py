from datetime import datetime

from flask_login import login_required, current_user

from . import main
from . import controller
from .. import db
from ..decorators import permission_required
from ..models import Roles


@main.before_request
def before_request():
    # update last active
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


# Unauthorized

@main.route("/")
@main.route("/all-blogs/")
@main.route("/all-blogs/<int:page>", methods=["GET", "POST"])
def all_blogs(page=1):
    return controller.all_blogs(page)


@main.route("/blog/<int:id>", methods=["POST", "GET"])
def blog(id):
    return controller.blog(id)



@main.route("/profile/<int:id>", methods=["GET", "POST"])
def profile(id):
    return controller.profile(id)


@main.route("/load/avatar/<int:id>", methods=["GET"])
def load_avatar(id):
    return controller.load_avatar(id)


@main.route("/load/blog/<int:id>/preview_image", methods=["GET"])
def load_blog_preview_image(id):
    return controller.load_blog_preview_image(id)


# Authorized

@main.route("/my-blogs/")
@main.route("/my-blogs/<int:page>", methods=["GET", "POST"])
@login_required
def my_blogs(page=1):
    return controller.my_blogs(page)


@main.route("/create-blog", methods=["GET", "POST"])
@login_required
def create_blog():
    return controller.create_blog()


@main.route("/upload/avatar", methods=["POST"])
@login_required
def upload_avatar():
    return controller.upload_avatar()



