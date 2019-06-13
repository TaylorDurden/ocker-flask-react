# from datetime import datetime
import datetime, json
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash
from project import db
from project.config import BaseConfig
import jwt
from flask import url_for

article_tags = db.Table('article_tags',
                     db.Column('follower_id',
                               db.Integer,
                               db.ForeignKey('user.id')),
                     db.Column('followed_id',
                               db.Integer,
                               db.ForeignKey('user.id')),
                     )


class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(128), nullable=False)
    body = db.Column(db.Text(), nullable=False)
    author_name = db.Column(db.String(128))
    tags = db.relationship('tag', backref='articles', lazy='dynamic')
    open_comment = db.Column(db.Boolean(), default=True, nullable=False)
    created_date = db.Column(db.DateTime, default=func.now(), nullable=False)
    last_edit_date = db.Column(db.DateTime, default=func.now(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    like_count = db.Column(db.Integer)
    fav_count = db.Column(db.Integer)
    visit_count = db.Column(db.Integer)
    comments = db.relationship('comment', backref='article', lazy='dynamic')
    tags = db.relationship(
        'tag', secondary=article_tags,
        backref=db.backref('articles', lazy='dynamic'), lazy='dynamic')
    pass


class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(128), nullable=False)
    pass


class ArticleTags(db.Model):
    __tablename__ = "article_tags"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)
    pass


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(4000), nullable=False)

    pass
