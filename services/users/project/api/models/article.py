# from datetime import datetime
import datetime, json
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash
from project import db
from project.config import BaseConfig
import jwt
from flask import url_for


class Article(db.Model):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(128), nullable=False)
    body = db.Column(db.Text())

    pass


class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(128), nullable=False)
    pass


class Category(db.Model):
    pass


class Comment(db.Model):
    pass
