# _*_ coding: utf-8 _*_
__author__ = 'taylor'
__date__ = '2019/4/14 11:22 PM'

import jwt, datetime, time
from flask import jsonify
from project.api.models import User
from project import create_app, config, db


class Auth():
    @staticmethod
    def encode_auth_token(user_id, login_time):
        """
        生成认证token
        :param user_id: int 
        :param login_time: int(timestamp)
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=10),  # 过期时间
                'iat': datetime.datetime.utcnow(),  # 发行时间
                'iss': 'taylor',  # token签发者
                'data': {
                    'id': user_id,
                    'login_time': login_time
                }
            }
            return jwt.encode(
                payload,
                config.BaseConfig.SECRET_KEY,
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        验证Token
        :param auth_token:
        :return: integer|string
        """
        try:
            # payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'), leeway=datetime.timedelta(seconds=10))
            # 取消过期时间验证
            payload = jwt.decode(auth_token, config.SECRET_KEY, options={'verify_exp': False})
            if ('data' in payload and 'id' in payload['data']):
                return payload
            else:
                raise jwt.InvalidTokenError
        except jwt.ExpiredSignatureError:
            return 'Token过期'
        except jwt.InvalidTokenError:
            return '无效Token'

    def authenticate(self, username, password):
        """
        用户登录，登录成功返回token，写将登录时间写入数据库；登录失败返回失败原因
        :param password:
        :return: json
        """
        user = User.query.filter_by(username=username).first()
        if user is None:
            return jsonify({
                'status': 404,
                'data': '',
                'msg': '找不到该用户'
            })
        else:
            if user.check_password(password):
                login_time = int(time.time())
                user.login_time = login_time
                db.session.commit()
                token = self.encode_auth_token(user.id, login_time)
                return jsonify({
                    'status': 200,
                    'data': token.decode(),
                    'msg': '登录成功!'
                })
            else:
                return jsonify({
                    'status': 401,
                    'data': '',
                    'msg': '密码错误!'
                })

    def identify(self, request):
        """
        用户鉴权
        :return: list
        """
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_tokens = auth_header.split(" ")
            if not auth_tokens or auth_tokens[0] != 'JWT' or len(auth_tokens) != 2:
                result = jsonify({
                    'status': 401,
                    'data': '',
                    'msg': '密码错误!'
                })
            else:
                auth_token = auth_tokens[1]
                payload = self.decode_auth_token(auth_token)
                if not isinstance(payload, str):
                    user = User.get(payload['data']['id'])
                    if user is None:
                        result = jsonify({
                            'status': 404,
                            'data': '',
                            'msg': '找不到该用户'
                        })
                    else:
                        if user.login_time == payload['data']['login_time']:
                            result = jsonify({
                                'status': 200,
                                'data': user.id,
                                'msg': '认证成功!'
                            })
                        else:
                            result = jsonify({
                                'status': 401,
                                'data': user.id,
                                'msg': '登录token已失效，请重新登录!'
                            })
                else:
                    result = jsonify({
                        'status': 401,
                        'data': '',
                        'msg': payload
                    })
        else:
            result = jsonify({
                'status': 401,
                'data': '',
                'msg': '未提供有效token'
            })
        return result
