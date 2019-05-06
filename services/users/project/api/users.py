# _*_ coding: utf-8 _*_
from werkzeug.datastructures import MultiDict, ImmutableMultiDict

__author__ = 'taylor'
__date__ = '2019/3/17 3:52 AM'

# services/users/project/api/users.py

from flask import Blueprint, jsonify, request, render_template, json
from project.api.models import User
from project import db
from sqlalchemy import exc, and_, text
from project.config import BaseConfig
from datetime import datetime

users_blueprint = Blueprint('users', __name__, template_folder='./templates')


@users_blueprint.route('/users/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })


@users_blueprint.route('/users', methods=['POST'])
def add_user():
    post_data = request.get_json()
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }
    if not post_data:
        return jsonify(response_object), 400

    username = post_data.get('username')
    email = post_data.get('email')
    try:
        user = User.query.filter_by(email=email).first()
        if not user:
            db.session.add(User(username=username, email=email))
            db.session.commit()
            response_object['status'] = 'success'
            response_object['message'] = f'{email} was added!'
            return jsonify(response_object), 201
        else:
            response_object['message'] = 'Sorry. That email already exists.'
            return jsonify(response_object), 400
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify(response_object), 400


@users_blueprint.route('/users/<user_id>', methods=['GET'])
def get_single_user(user_id):
    """Get single user details"""
    response_object = {
        'status': 'fail',
        'message': 'User does not exist'
    }
    try:
        user = User.query.filter_by(id=int(user_id)).first()
        if not user:
            response_object['message'] = 'User does not exist'
            return jsonify(response_object), 404
        else:
            response_object = {
                'status': 'success',
                'data': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'active': user.active
                }
            }
            return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404


@users_blueprint.route('/users', methods=['GET'])
def get_all_users():
    """Get all users"""
    print(f"request args: {request.args}")
    username = request.args.get('username', "", type=str)
    current_page = request.args.get('current_page', 1, type=int)
    page_size = min(request.args.get('page_size', BaseConfig.LIST_PER_PAGE, type=int), 100)
    active = False if request.args.get('status', 1, type=int) == 0 else True;
    # 2019-04-30T16:09:38.998Z
    start_date = request.args.getlist('last_edit_date[0]')
    end_date = request.args.getlist('last_edit_date[1]')
    if len(start_date) and len(end_date):
        start_date = start_date[0]
        end_date = end_date[0]
    print(start_date)
    print(end_date)
    datetime_format = "%Y-%m-%d %H:%M:%S"
    sort_by = request.args.get('sort_by', "", type=str)
    order = request.args.get('order', "", type=str)
    query = User.query.filter(User.active == active)
    if username:
        query = User.query.filter(User.username.like(f"%{username}%"))
    if start_date and end_date:
        # self.last_edit_date.isoformat() + 'Z'
        query = User.query.filter(User.last_edit_date.between(start_date, end_date))
    query = _build_users_order_by_query(query, sort_by, order)
    response_object = User.to_collection_dict(query, current_page, page_size, 'users.get_all_users')
    return jsonify(response_object), 200


def _build_users_order_by_query(query, sort_by, order):
    # if sort_by == "last_seen":
    #     if order == "ascend":
    #         query = query.order_by(User.last_edit_date)
    #     else:
    #         query = query.order_by(User.last_edit_date.desc())
    # return query
    if sort_by:
        if order == "ascend":
            query = query.order_by(text(f"{sort_by}"))
        else:
            query = query.order_by(text(f"{sort_by} desc"))
    return query


@users_blueprint.route('/', methods=['GET'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        db.session.add(User(username=username, email=email))
        db.session.commit()
    users = User.query.all()
    return render_template('index.html', users=users)