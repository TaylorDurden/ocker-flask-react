from flask import Blueprint, jsonify, request, render_template, json
from project.api.models import User, Role
from project.api.model.article import Article
from sqlalchemy import exc, and_, text, func
from project.config import BaseConfig
from datetime import datetime
from operator import itemgetter, attrgetter
from project.utils.Role_Module_Permission import PermissionGroupList

articles_blueprint = Blueprint('articles', __name__, template_folder='../templates')


@articles_blueprint.route('/articles', methods=['GET'])
def get_paged_articles():
    current_page = request.args.get('current_page', 1, type=int)
    page_size = min(request.args.get('page_size', BaseConfig.LIST_PER_PAGE, type=int), 100)
    articles = Article.to_paged_dict(Article.query, current_page, page_size)
    return jsonify(articles), 200


@articles_blueprint.route('/articles/<article_id>', methods=['GET'])
def get_single_article(article_id):
    response_object = {
        'status': 'fail',
        'message': '文章不存在'
    }
    try:
        article = Article.query.filter_by(id=int(article_id)).first()
        if not article:
            return jsonify(response_object), 404
        else:
            response_object = {
                'status': 'success',
                'data': article.to_dict()
            }
            return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404


@articles_blueprint.route('/articles', methods=['POST'])
def add_article():
    post_data = request.get_json()
    response_object = {
        'status': 'fail',
        'message': '无效参数.'
    }
    if not post_data:
        return jsonify(response_object), 400

    title = post_data.get('title')
    content = post_data.get('content')
    author_name = post_data.get('author_name')
    tag_ids = post_data.get('tag_ids')
    # if role_ids and len(role_ids):
    #     role_ids = [int(x) for x in role_ids.split(',')]
    try:
        article = Article.query.filter_by(title=title).first()
        if not article:
            command = {'title': title, 'content': content, 'author_name': author_name, 'tag_ids': tag_ids}
            new_user = User.add_user(command)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            response_object['status'] = 'success'
            response_object['message'] = f'{email} was added!'
            return jsonify(response_object), 201
        else:
            response_object['message'] = 'Sorry. That email already exists.'
            return jsonify(response_object), 400
    except exc.IntegrityError:
        raise
        # db.session.rollback()
        # return jsonify(response_object), 400