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