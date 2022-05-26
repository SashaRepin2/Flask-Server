import uuid
from datetime import datetime
from enum import Enum

import bleach
import sqlalchemy
from flask_login import UserMixin
from sqlalchemy.orm import EXT_SKIP

from project import login_manager
from markdown import markdown
from project import db
from werkzeug.security import generate_password_hash, check_password_hash


class Roles(Enum):
    ADMIN = 'admin'
    USER = 'user'


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    permissions_level = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles_success_add = []

        for role in Roles:
            success = {'name': role, 'is_success': False}
            role_db = Role.query.filter_by(name=role.value).first()
            if role_db is None:
                role_db = Role(name=role.value, permissions_level=1)
                success['is_success'] = True
            db.session.add(role_db)
            roles_success_add.append(success)
        db.session.commit()

        return roles_success_add


class Follow(db.Model):
    __tablename__ = 'follows'

    # Fields
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                            primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                            primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Follow> {self.follower_id} follow {self.followed_id}"


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    # Fields
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    login = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    first_name = db.Column(db.String(25), nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    age = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    confirmed = db.Column(db.Boolean, nullable=True, default=True)  # For Test
    confirmed_link = db.Column(db.String(200), nullable=True)
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    avatar = db.Column(db.LargeBinary, default=None)

    # Relationships

    blogs = db.relationship('Blog', backref='author', lazy='dynamic')
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    followed = db.relationship('Follow',
                               foreign_keys=[Follow.follower_id],
                               backref=db.backref('follower', lazy='joined'),
                               lazy='dynamic',
                               cascade='all, delete-orphan')
    followers = db.relationship('Follow',
                                foreign_keys=[Follow.followed_id],
                                backref=db.backref('followed', lazy='joined'),
                                lazy='dynamic',
                                cascade='all, delete-orphan')
    comments = db.relationship('Comment', backref='author', lazy='dynamic')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            self.role = Role.query.filter_by(name=Roles.USER.value).first()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    def get_role(self):
        print(self.role_id)
        role = Role.query.filter_by(id=self.role_id).first()
        print(role)
        return role

    @password.setter
    def password(self, password):
        print(generate_password_hash(password))
        self.password_hash = generate_password_hash(password)
        print(self.password_hash)

    @staticmethod
    def get_user_with_email_and_password(email, password):
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            return user
        else:
            return None

    @staticmethod
    def get_user_by_activation_link(link):
        return User.query.filter_by(activationLink=link).first()

    @staticmethod
    def get_activation_link():
        return uuid.uuid4().hex

    @staticmethod
    def get_user_by_email(email):
        return User.query.filter_by(email=email).first()

    def set_user_avatar(self, binary_img):
        # if binary_img:
        self.avatar = binary_img

    def get_user_avatar(self):
        return self.avatar

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    def has_permissions(self, role):
        return self.role is not None and self.role.name == role

    def is_admin(self):
        return self.role.name == Roles.ADMIN.value

    def change_role(self, role):
        role = Role.query.filter_by(name=role).first()
        self.role_id = role.id

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<{self.id}> {self.email},  {self.login}"


class Blog(db.Model):
    __tablename__ = 'blogs'

    # Fields
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(25))
    description = db.Column(db.String(50))
    preview_image = db.Column(db.LargeBinary)
    content = db.Column(db.Text)
    content_html = db.Column(db.Text, default=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    is_accepted = db.Column(db.Boolean, default=False, server_default="0",
                            nullable=False)

    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Relationships
    comments = db.relationship('Comment', backref='blog', lazy='dynamic')

    @staticmethod
    def on_changed_content(target, value, oldvalue, initiator):
        if value == oldvalue:
            return EXT_SKIP

        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p', 'img', 'center']
        target.content_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))

    def __repr__(self):
        return f"<{self.id}> {self.title}, {self.author_id}"


# Event listener Blog Content changes
db.event.listen(Blog.content, 'set', Blog.on_changed_content, active_history=True, retval=True)


class Comment(db.Model):
    __tablename__ = 'comments'

    # Fields
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.id'))
