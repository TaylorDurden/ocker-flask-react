# from datetime import datetime
import datetime
from sqlalchemy.sql import func
from project import db
from project.config import BaseConfig
from project.api.mixin import PaginatedAPIMixin

article_tags = db.Table('article_tags',
                     db.Column('follower_id',
                               db.Integer,
                               db.ForeignKey('user.id')),
                     db.Column('followed_id',
                               db.Integer,
                               db.ForeignKey('user.id')),
                     )


class Article(db.Model, PaginatedAPIMixin):
    __tablename__ = 'article'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(128), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    author_name = db.Column(db.String(128))
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
    status = db.Column(db.Boolean(), default=False, nullable=False)
    feature_image = db.Column(db.String())

    def __repr__(self):
        return f'<Article {self.title}>'

    def get(self, article_id):
        return self.query.filter_by(id=article_id).first()

    def to_dict(self, include_fields=True):
        data = {
            'id': self.id,
            'key': self.id,
            'content': self.content,
            'author_name': self.author_name,
            'tags': [x.to_dict() for x in self.tags.all()],
            'open_comment': self.open_comment,
            'created_date': self.last_edit_date.isoformat() + 'Z',
            'last_edit_date': self.last_edit_date.isoformat() + 'Z',
            # 'username': self.author.name,
            'like_count': self.like_count,
            'fav_count': self.fav_count,
            'visit_count': self.visit_count,
            'status': self.status,
            'comment_count': self.comments.count(),
            'feature_image': self.feature_image,
        }
        # if include_fields:
        #     data['email'] = self.email
        #     data['role_ids'] = [x.id for x in self.roles]
        return data


class Tag(db.Model):
    __tablename__ = 'tag'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)
    slug = db.Column(db.String(128))
    created_date = db.Column(db.DateTime, default=func.now(), nullable=False)
    last_edit_date = db.Column(db.DateTime, default=func.now(), nullable=False)

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
        }
        return data


class ArticleTags(db.Model):
    __tablename__ = "article_tags"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)


class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), nullable=False)
    count = db.Column(db.Integer)
    desc = db.Column(db.String(128))
    parent = db.relationship('category', backref='children', lazy='dynamic')
    created_date = db.Column(db.DateTime, default=func.now(), nullable=False)
    last_edit_date = db.Column(db.DateTime, default=func.now(), nullable=False)

    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'desc': self.desc,
            'count': self.count,
            # 'parent': self.children,
        }
        return data


class Comment(db.Model, PaginatedAPIMixin):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    created_date = db.Column(db.DateTime, default=func.now(), nullable=False)
    last_edit_date = db.Column(db.DateTime, default=func.now(), nullable=False)

    def to_dict(self):
        data = {
            'id': self.id,
            'content': self.content,
            'desc': self.desc,
            'count': self.count,
            # 'parent': self.children,
        }
        return data

