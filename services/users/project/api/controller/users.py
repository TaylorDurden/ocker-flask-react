# _*_ coding: utf-8 _*_
from werkzeug.datastructures import MultiDict, ImmutableMultiDict

__author__ = 'taylor'
__date__ = '2019/3/17 3:52 AM'

# services/users/project/api/users.py

from flask import Blueprint, jsonify, request, render_template, json
from project.api.models import User
from project import db
from sqlalchemy import exc, and_, text, func
from project.config import BaseConfig
from datetime import datetime
from operator import itemgetter, attrgetter

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
    status = False if request.args.get('status', 1, type=int) == 0 else True
    # 用户列表表头上的状态多选
    active = request.args.get('active', "", type=str)
    active_list = active.split(',') if len(active) else ""
    # 2019-04-30T16:09:38.998Z
    start_date = request.args.getlist('last_edit_date[0]')
    end_date = request.args.getlist('last_edit_date[1]')
    if len(start_date) and len(end_date):
        start_date = start_date[0]
        end_date = end_date[0]
    print(start_date)
    print(end_date)
    sort_by = request.args.get('sort_by', "", type=str)
    order = request.args.get('order', "", type=str)

    query = db.session.query(User).filter(User.active == status)
    if len(active_list):
        query = db.session.query(User).filter(User.active.in_(active_list))
    if username:
        query = db.session.query(User).filter(User.username.like(f"%{username}%"))
    if start_date and end_date:
        # self.last_edit_date.isoformat() + 'Z'
        query = db.session.query(User).filter(User.last_edit_date.between(start_date, end_date))
    print(query)
    response_object = User.to_paged_dict(query, current_page, page_size, 'users.get_all_users')
    print("response_object", response_object)
    sort_keys = {
        'last_edit_date': 4,
        'post_count': 5,
        'follower_count': 6,
        'followed_count': 7,
    }
    if sort_by:
        print("sorted: ", sorted(response_object['list'], key=itemgetter(sort_by), reverse=order != "ascend"))
        # response_object['list'] = sorted(response_object['list'], key=itemgetter(sort_by), reverse=order != "ascend")
        response_object['list'] = sorted(response_object['list'], key=lambda x : x[sort_by], reverse=order != "ascend")
    return jsonify(response_object), 200


@users_blueprint.route('/users/index', methods=['GET'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        db.session.add(User(username=username, email=email))
        db.session.commit()
    users = User.query.all()
    return render_template('index.html', users=users)


@users_blueprint.route('/users/batch-inactive', methods=['POST'])
def batch_inactive():   
    if request.method == 'POST':
        keys = request.form['key']
        users = User.query.all()
        # [user for user in users]
        # db.session.commit()
    return render_template('index.html', users=users)