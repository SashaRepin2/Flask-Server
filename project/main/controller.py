import os

from flask import render_template, url_for, request, make_response, flash, current_app
from flask_login import current_user
from werkzeug.utils import redirect

from project import db
from project.main.forms import BlogForm
from project.models import User, Blog, Follow


def profile(id):
    user = User.query.get_or_404(id)
    return render_template('profile.html', user=user)


def all_blogs(page):
    blogs_per_page = int(os.environ.get('BLOGS_PER_PAGE'))
    pagination = Blog.query.paginate(page, blogs_per_page, error_out=False)
    blogs = pagination.items
    return render_template('blogs.html', blogs=blogs, pagination=pagination)


def my_blogs(page):
    blogs_per_page = int(os.environ.get('BLOGS_PER_PAGE'))
    pagination = Blog.query.filter_by(author_id=current_user.id).paginate(page, blogs_per_page, error_out=False)
    blogs = pagination.items
    return render_template('blogs.html', blogs=blogs, pagination=pagination)


def create_blog():
    form = BlogForm()
    if form.validate_on_submit():
        print(form.preview_image.data)
        image_data = request.files[form.preview_image.name].read()

        post = Blog(title=form.title.data, preview_image=image_data, description=form.description.data,
                    content=form.content.data,
                    author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('main.all_blogs'))

    return render_template('./blog/create_blog.html', title='Create blog', form=form)


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def upload_avatar():
    # Check files in request
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

            except FileNotFoundError as e:
                flash('Ошибка при чтении файла', "loadavatar")

        else:
            print('request dont have files')
            flash('Ошибка загрузки аватара', "loadavatar")
    return redirect(url_for('main.profile', id=current_user.id))


def load_avatar(id):
    user = User.query.filter_by(id=id).first()

    if not user:
        return ""

    img = user.avatar
    if not img:
        try:
            with current_app.open_resource(current_app.root_path + url_for('static', filename='img/avatar/default.png'),
                                           "rb") as f:
                img = f.read()
        except FileNotFoundError as e:
            return ""

    h = make_response(img)
    h.headers['Content-Type'] = 'image/png'
    return h


def load_blog_preview_image(id):
    blog = Blog.query.filter_by(id=id).first()

    if not blog:
        return ""

    img = blog.preview_image
    if not img:
        try:
            with current_app.open_resource(current_app.root_path + url_for('static', filename='img/avatar/default.png'),
                                           "rb") as f:
                img = f.read()
        except FileNotFoundError as e:
            return ""

    h = make_response(img)
    h.headers['Content-Type'] = 'image/png'
    return h
