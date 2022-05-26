import os

from flask import render_template, url_for
from flask_login import current_user
from werkzeug.utils import redirect

from project import db
from project.admin.forms import GetAdminRole, AcceptedBlogForm
from project.models import Roles, Role, Blog


def admin_panel(page):
    blogs_per_page = int(os.environ.get('BLOGS_PER_PAGE'))
    pagination = Blog.query.filter_by(is_accepted=False).order_by(Blog.timestamp.desc()).paginate(page, blogs_per_page,
                                                                                                  error_out=False)
    blogs = pagination.items
    return render_template('blogs.html', blogs=blogs, pagination=pagination)


def get_admin_role():
    form = GetAdminRole()

    if form.validate_on_submit():
        role = Role.query.filter_by(name=Roles.ADMIN.value).first()
        current_user.role_id = role.id
        db.session.commit()

        return redirect(url_for('main.profile', id=current_user.id))

    return render_template('./admin/get_role.html', form=form)


def accepted_blog(id):
    form = AcceptedBlogForm()
    blog = Blog.query.get_or_404(id)
    print(f'Es {form.accepted.data}')
    print(f"Val {form.validate_on_submit()}")
    print(form.errors)

    if form.validate_on_submit():
        print(f'Es {form.accepted.data}')
        blog.is_accepted = form.accepted.data
        db.session.commit()

    return redirect(url_for('main.blog', id=id))
