import uuid
from datetime import datetime

from flask_login import UserMixin, AnonymousUserMixin
from project import login_manager

from project import db
from werkzeug.security import generate_password_hash, check_password_hash


class Follow(db.Model):
    __tablename__ = 'follows'
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                            primary_key=True)
    followed_id = db.Column(db.Integer, db.ForeignKey('users.id'),
                            primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<{self.follower_id}> {self.followed_id}"


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    login = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    age = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    isActivated = db.Column(db.Boolean, nullable=False, default=False)
    activationLink = db.Column(db.String(200), nullable=False)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
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

    # profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'),
    #                        nullable=False)
    # profile = db.relationship('Profile',
    #                           backref=db.backref('users_profile', lazy=True))
    #
    # token_id = db.Column(db.Integer, db.ForeignKey('token.id'),
    #                      nullable=False)
    # token = db.relationship('Token',
    #                         backref=db.backref('users_token', lazy=True))

    def __init__(self, email, login, first_name, last_name, age, gender, password):
        self.email = email
        self.last_name = last_name
        self.first_name = first_name
        self.login = login
        self.age = age
        self.gender = gender
        self.password_hash = User.hashed_password(password)
        self.activationLink = User.get_activation_link()

    def __repr__(self):
        return f"<{self.id}> {self.email},  {self.login}"

    @staticmethod
    def hashed_password(password):
        return generate_password_hash(password)

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

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


#
# class Profile(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50), nullable=False)
#     role = db.Column(db.String(30), default='default', nullable=False)
#     date_created = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
#
#     def __init__(self, name):
#         self.name = name
#
#     def __repr__(self):
#         return f"<{self.id}>  {self.name}, {self.role}, {self.date_created}, {self.user_id}"
#
#
# class Token(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     refresh_token = db.Column(db.String(100), nullable=True)
#
#     def __init__(self, ip_address, refresh_token):
#         self.ip_address = ip_address
#         self.refresh_token = refresh_token
#
#     def __repr__(self):
#         return f"<{self.id}>  {self.ip_address}, {self.refresh_token}, {self.user_id}"
class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f"<{self.id}> {self.title}, {self.body},{self.timestamp},{self.author_id}"
