import os

from flask import render_template, url_for, request, make_response, flash
from flask_login import current_user
from werkzeug.utils import redirect, secure_filename

from project import db
from project.main.forms import PostForm
from project.models import User, Blog, Follow


def home():
    return render_template('home.html')


def profile(user_id):
    user = User.query.filter_by(id=user_id).first()
    return render_template('profile.html', user=user)


# HOME PAGE WITH ALL BLOGS
def all_blogs(page):
    blogs_per_page = int(os.environ.get('BLOGS_PER_PAGE'))
    pagination = Blog.query.paginate(page, blogs_per_page, error_out=False)
    blogs = pagination.items
    return render_template('posts.html', blogs=blogs, pagination=pagination)


# CREATE A BLOG
def create_blog():
    form = PostForm()
    if form.validate_on_submit():
        post = Blog(title=form.title.data, body=form.body.data,
                    author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.all_posts', page=1))

    return render_template('./blog/create_blog.html', form=form)


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


# Проверка, что файл есть
# ПРоверка имени и размера файла
# Загрузка файла в бд
def upload_avatar():
    # Check files in request
    msg = ''
    if request.method == 'POST':
        file = request.files['file']
        # Check filename and extension
        if file and allowed_file(file.filename):
            try:
                # Upload image in DB
                file_data = file.read()
                current_user.avatar = file_data
                db.session.add(current_user._get_current_object())
                db.session.commit()
                msg = 'okay'
            except FileNotFoundError as e:
                msg = 'Ошибка при чтении файла'
                flash('Ошибка при чтении файла')

        else:
            print('request dont have files')
            msg = 'request dont have files'
            flash('Ошибка загрузки аватара')
    return msg


# # Get a file from request
# file = request.files['file']
# if file.filename == '':
#     flash('No selected file')


def load_avatar(id):
    user = User.query.filter_by(id=id).first()
    img = user.avatar
    if not user.avatar:
        return ""

    h = make_response(img)
    h.headers['Content-Type'] = 'image/png'
    return h
