# _*_ coding: utf-8 _*_
__author__ = 'taylor'
__date__ = '2019/3/17 3:52 AM'

# services/users/project/api/models.py

# from datetime import datetime
import datetime, json
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash
from project import db
from project.config import BaseConfig
import jwt
from flask import url_for
from hashlib import md5
from project.utils.Role_Module_Permission import Module

# from project.api.mixin import PaginatedAPIMixin

followers = db.Table('followers',
                     db.Column('follower_id',
                               db.Integer,
                               db.ForeignKey('user.id')),
                     db.Column('followed_id',
                               db.Integer,
                               db.ForeignKey('user.id'))
                     )

user_roles = db.Table('user_roles',
                      db.Column('user_id',
                                db.Integer,
                                db.ForeignKey('user.id')),
                      db.Column('role_id',
                                db.Integer,
                                db.ForeignKey('role.id'))
                      )


class PaginatedAPIMixin(object):
    @staticmethod
    def to_paged_dict(query, page, per_page, include_fields=True, endpoint=None, **kwargs):
        resources = query.paginate(page, per_page, False)
        data = {
            'list': [item.to_dict(include_fields) for item in resources.items],
            'pagination': {
                'current': page,
                'pageSize': per_page,
                'total_pages': resources.pages,
                'total': resources.total
            }
        }
        if endpoint:
            data['_links'] = {
                'self': url_for(endpoint, page=page, per_page=per_page,
                                **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page,
                                **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page,
                                **kwargs) if resources.has_prev else None
            }
        return data


class User(PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), nullable=False)
    nickname = db.Column(db.String(64), index=True)
    password_hash = db.Column(db.String(128))
    openid = db.Column(db.String(64))
    email = db.Column(db.String(120), index=True, unique=True)
    phone = db.Column(db.String(120), index=True, unique=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    roles = db.relationship(
        'Role', secondary=user_roles,
        primaryjoin=(user_roles.c.user_id == id),
        backref=db.backref('roles', lazy='dynamic'), lazy='dynamic')
    avatar = db.Column(db.String())
    active = db.Column(db.Boolean(), default=True, nullable=False)
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')
    is_admin = db.Column(db.Boolean(), default=False)
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

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

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

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def to_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'active': self.active
        }

    def to_dict(self, include_email):
        data = {
            'id': self.id,
            'key': self.id,
            'username': self.username,
            'active': self.active,
            'last_edit_date': self.last_edit_date.isoformat() + 'Z',
            'post_count': self.posts.count(),
            'follower_count': self.followers.count(),
            'followed_count': self.followed.count(),
            '_links': {
                'self': url_for('users.get_single_user', user_id=self.id),
                'avatar': self.avatar(128)
            }
        }
        if include_email:
            data['email'] = self.email
        return data

    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        :param user_id: 
        :return: 
        :return: token string
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


class Role(db.Model, PaginatedAPIMixin):
    """
    Role
    """

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)
    desc = db.Column(db.String(256))
    # lazy="dynamic" 只可以用在一对多和多对多关系中，不可以用在一对一和多对一中。
    permissions = db.relationship('RolePermission', backref='role', lazy='dynamic')

    def to_dict(self, include_permissions=True):
        data = {
            'id': self.id,
            'name': self.name,
            'desc': self.desc,
        }
        if include_permissions:
            permissions = {}
            for x in self.permissions:
                str_vals = x.permissions.split(',')
                permissions[int(x.name)] = [int(x) for x in str_vals]
                #permissions[int(x.name)].key = int(x.name)

            data['permissions'] = permissions

        return data

    @staticmethod
    def new_role(command):
        role = Role()
        role.name = command['name']
        role.desc = command['desc']
        print(command['permissions'])
        for key, value in command['permissions'].items():
            print(key, value)
            name = key
            permissions = ",".join([json.dumps(x) for x in value])
            print(name, permissions)
            role.permissions.append(RolePermission(name=name, permissions=permissions))
        return role

    def edit(self, command):
        self.name = command['name']
        self.desc = command['desc']
        [x.delete() for x in self.permissions]
        for key, value in command['permissions'].items():
            name = key
            permissions = ",".join([json.dumps(x) for x in value])
            self.permissions.append(RolePermission(name=name, permissions=permissions))


class RolePermission(db.Model):
    """
    Role_Permission
    """
    __tablename__ = 'role_permission'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Integer, nullable=False)
    permissions = db.Column(db.String(256))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
