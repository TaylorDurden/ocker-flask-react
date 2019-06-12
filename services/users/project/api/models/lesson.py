# from datetime import datetime
import datetime, json
from sqlalchemy.sql import func
from werkzeug.security import generate_password_hash, check_password_hash
from project import db
from project.config import BaseConfig
import jwt
from flask import url_for


class Lesson(db.Model):
    pass


class LessonChapter(db.Model):
    pass


class LessonChapterItem(db.Model):
    pass


class LessonQuestion(db.Model):
    pass


class LessonAnswer(db.Model):
    pass
