# _*_ coding: utf-8 _*_
__author__ = 'taylor'
__date__ = '2019/3/17 3:52 AM'

# services/users/project/api/models.py

# from datetime import datetime
import datetime
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash
from project import db
from project.config import BaseConfig
import jwt

followers = db.Table('followers',
                     db.Column('follower_id',
                               db.Integer,
                               db.ForeignKey('user.id')),
                     db.Column('followed_id',
                               db.Integer,
                               db.ForeignKey('user.id'))
                     )


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), nullable=False)
    nickname = db.Column(db.String(64), index=True)
    password_hash = db.Column(db.String(128))
    openid = db.Column(db.String(64))
    email = db.Column(db.String(120), index=True, unique=True)
    phone = db.Column(db.String(120), index=True, unique=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    avatar = db.Column(db.String(256))
    active = db.Column(db.Boolean(), default=True, nullable=False)
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')
    created_date = db.Column(db.DateTime, default=func.now(), nullable=False)
    last_edit_date = db.Column(db.DateTime, default=func.now(), nullable=False)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get(self, id):
        return self.query.filter_by(id=id).first()

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def un_follow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id
        ).count() > 0

    def to_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'active': self.active
        }

    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                BaseConfig.SECRET_KEY,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, BaseConfig.SECRET_KEY)
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    like_count = db.Column(db.Integer)
    visit_count = db.Column(db.Integer)
    created_date = db.Column(db.DateTime, default=func.now(), nullable=False)
    last_edit_date = db.Column(db.DateTime, default=func.now(), nullable=False)

    def __repr__(self):
        return '<Post {}>'.format(self.body)


class BlacklistToken(db.Model):
    """
    Token model for storing JWT tokens
    """
    __tablename__ = 'blacklist_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()

    def __repr__(self):
        return f'<id: token: {self.token}>'

    @staticmethod
    def check_blacklist(auth_token):
        # check whether auth token has been blacklisted
        response = BlacklistToken.query.filter_by(token=str(auth_token)).first()
        if response:
            return True
        else:
            return False
