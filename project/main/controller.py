import os

from flask import render_template, url_for, request
from flask_login import current_user
from werkzeug.utils import redirect

from project import db
from project.main.forms import PostForm
from project.models import User, Post, Follow


def index(user_id):
    user = User.query.filter_by(id=user_id).first()
    return render_template('index.html', user=user)
# , followers=user.followed


def all_posts(page):
    posts_per_page = int(os.environ.get('POSTS_PER_PAGE'))
    pagination = Post.query.paginate(page, posts_per_page, error_out=False)
    posts = pagination.items
    return render_template('posts.html', posts=posts, pagination=pagination)


def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, body=form.body.data,
                    author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.all_posts', page=1))

    return render_template('create_post.html', form=form)
