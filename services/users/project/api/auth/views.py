# _*_ coding: utf-8 _*_
__author__ = 'taylor'
__date__ = '2019/4/15 11:29 PM'

from flask import Blueprint, request, make_response, jsonify
from flask.views import MethodView

from project import db
from project.api.models import User


auth_blueprint = Blueprint('auth', __name__)


class RegisterAPI(MethodView):
    """
    用户注册 Resource
    """

    def post(self):
        post_data = request.get_json()
        user = User.query.filter_by(email=post_data.get('email')).first()
        if not user:
            try:
                user = User(
                    username=post_data.get('username'),
                    email=post_data.get('email')
                )
                password = post_data.get('password')
                user.set_password(password)

                db.session.add(user)
                db.session.commit()

                auth_token = user.encode_auth_token(user.id)
                responseObject = {
                    'status': 'success',
                    'message': '注册成功.',
                    'auth_token': auth_token.decode()
                }
                return make_response(jsonify(responseObject)), 201
            except Exception as e:
                responseObject = {
                    'status': 'fail',
                    'message': '出错了，请重试.'
                }
                return make_response(jsonify(responseObject)), 401
        else:
            responseObject = {
                'status': 'fail',
                'message': '用户已存在，请登录.',
            }
            return make_response(jsonify(responseObject)), 202


# define the API resources
registration_view = RegisterAPI.as_view('register_api')

# add Rules for API Endpoints
auth_blueprint.add_url_rule(
    '/auth/register',
    view_func=registration_view,
    methods=['POST']
)