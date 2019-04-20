# _*_ coding: utf-8 _*_
__author__ = 'taylor'
__date__ = '2019/4/15 11:32 PM'

import unittest
import time
from project import db
from project.api.models import User, BlacklistToken
from project.tests.base import BaseTestCase
import json

JSON_CONTENT_TYPE = 'application/json'
SUCCESS = 'success'
FAIL = 'fail'
REGISTER_SUCCESS = '注册成功.'
LOG_IN_SUCCESS = '登录成功.'
USERNAME = 'taylor'
EMAIL = 'taylor@gmail.com'
PASSWORD = '123456'


def register_user(self, username, email, password):
    return self.client.post(
        '/auth/register',
        data=json.dumps(dict(
            username=username,
            email=email,
            password=password
        )),
        content_type=JSON_CONTENT_TYPE,
    )


class TestAuthBlueprint(BaseTestCase):
    def test_registration(self):
        """ 0001 Test for user registration"""
        with self.client:
            response = register_user(self, username=USERNAME, email=EMAIL, password=PASSWORD)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == SUCCESS)
            self.assertTrue(data['message'] == REGISTER_SUCCESS)
            self.assertTrue(data['auth_token'])
            self.assertTrue(response.content_type == JSON_CONTENT_TYPE)
            self.assertEqual(response.status_code, 201)

    def test_registered_with_already_registered_user(self):
        """ 0002 Test registration with already registered email """
        user = User(
            username=USERNAME,
            email=EMAIL,
        )
        db.session.add(user)
        db.session.commit()
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps(dict(
                    username=USERNAME,
                    email=EMAIL,
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(
                data['message'] == '用户已存在，请登录.'
            )
            self.assertTrue(response.content_type == JSON_CONTENT_TYPE)
            self.assertEqual(response.status_code, 202)

    def test_registered_user_login(self):
        """ 0003 Test for login of registered-user login """
        with self.client:
            # user registration
            response_register = register_user(self, username=USERNAME, email=EMAIL, password=PASSWORD)
            data_register = json.loads(response_register.data.decode())
            self.assertTrue(data_register['status'] == 'success')
            self.assertTrue(
                data_register['message'] == REGISTER_SUCCESS
            )
            self.assertTrue(data_register['auth_token'])
            self.assertTrue(response_register.content_type == JSON_CONTENT_TYPE)
            self.assertEqual(response_register.status_code, 201)
            # registered user login
            response = self.client.post(
                '/auth/login',
                data=json.dumps(dict(
                    email=EMAIL,
                    password=PASSWORD
                )),
                content_type=JSON_CONTENT_TYPE
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == SUCCESS)
            self.assertTrue(data['message'] == LOG_IN_SUCCESS)
            self.assertTrue(data['auth_token'])
            self.assertTrue(response.content_type == JSON_CONTENT_TYPE)
            self.assertEqual(response.status_code, 200)

    def test_non_registered_user_login(self):
        """ 0004 Test for login of non-registered user """
        with self.client:
            response = self.client.post(
                '/auth/login',
                data=json.dumps(dict(
                    email=EMAIL,
                    password=PASSWORD
                )),
                content_type=JSON_CONTENT_TYPE,
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == FAIL)
            self.assertTrue(data['message'] == '用户不存在.')
            self.assertTrue(response.content_type == JSON_CONTENT_TYPE)
            self.assertEqual(response.status_code, 404)

    def test_user_status(self):
        """ 0005 Test for  user status """
        with self.client:
            response_register = register_user(self, username=USERNAME, email=EMAIL, password=PASSWORD)
            response = self.client.get(
                '/auth/status',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        response_register.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == SUCCESS)
            self.assertTrue(data['data'] is not None)
            self.assertTrue(data['data']['email'] == EMAIL)
            self.assertTrue(data['data']['active'] is 'true' or 'false')
            self.assertTrue(data['data']['created_date'] is not None)
            self.assertEqual(response.status_code, 200)

    def test_valid_logout(self):
        """ 0006 Test for logout before token expires """
        with self.client:
            # user registration
            response_register = register_user(self, username=USERNAME, email=EMAIL, password=PASSWORD)
            data_register = json.loads(response_register.data.decode())
            self.assertTrue(data_register['status'] == SUCCESS)
            self.assertTrue(
                data_register['message'] == REGISTER_SUCCESS
            )
            self.assertTrue(data_register['auth_token'])
            self.assertTrue(response_register.content_type == JSON_CONTENT_TYPE)
            self.assertTrue(response_register.status_code, 201)

            # user login
            response_login = self.client.post(
                '/auth/login',
                data=json.dumps(dict(
                    email=EMAIL,
                    password=PASSWORD
                )),
                content_type=JSON_CONTENT_TYPE,
            )
            data_login = json.loads(response_login.data.decode())
            self.assertTrue(data_login['status'] == SUCCESS)
            self.assertTrue(data_login['message'] == LOG_IN_SUCCESS)
            self.assertTrue(data_register['auth_token'])
            self.assertTrue(response_login.content_type == JSON_CONTENT_TYPE)
            self.assertEqual(response_login.status_code, 200)
            # valid token logout
            response_logout = self.client.post(
                '/auth/logout',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        response_login.data.decode()
                    )['auth_token']
                )
            )
            # print(f'logout data:{response_logout}')
            data = json.loads(response_logout.data.decode())
            self.assertTrue(data['status'] == SUCCESS)
            self.assertTrue(data['message'] == '登出成功.')
            self.assertEqual(response_logout.status_code, 200)

    def test_invalid_logout(self):
        """ 0007 Testing logout after the token expires """
        with self.client:
            # user registration
            response_register = register_user(self, username=USERNAME, email=EMAIL, password=PASSWORD)
            data_register = json.loads(response_register.data.decode())
            self.assertTrue(data_register['status'] == SUCCESS)
            self.assertTrue(
                data_register['message'] == REGISTER_SUCCESS
            )
            self.assertTrue(data_register['auth_token'])
            self.assertTrue(response_register.content_type == JSON_CONTENT_TYPE)
            self.assertTrue(response_register.status_code, 201)

            # user login
            response_login = self.client.post(
                '/auth/login',
                data=json.dumps(dict(
                    email=EMAIL,
                    password=PASSWORD
                )),
                content_type=JSON_CONTENT_TYPE,
            )
            data_login = json.loads(response_login.data.decode())
            self.assertTrue(data_login['status'] == SUCCESS)
            self.assertTrue(data_login['message'] == LOG_IN_SUCCESS)
            self.assertTrue(data_register['auth_token'])
            self.assertTrue(response_login.content_type == JSON_CONTENT_TYPE)
            self.assertEqual(response_login.status_code, 200)

            # invalid token logout
            time.sleep(6)
            response_logout = self.client.post(
                '/auth/logout',
                headers=dict(
                    Authorization=f"Bearer {json.loads(response_login.data.decode())['auth_token']}"
                )
            )
            data = json.loads(response_logout.data.decode())
            self.assertTrue(data['status'] == 'fail')
            print(f'logout data:{data}')
            self.assertTrue(data['message'] == 'Signature expired. Please log in again.')
            self.assertEqual(response_logout.status_code, 401)

    def test_valid_blacklisted_token_logout(self):
        """ 0008 Test for logout after a valid token gets blacklisted """
        with self.client:
            # user registration
            response_register = register_user(self, username=USERNAME, email=EMAIL, password=PASSWORD)
            data_register = json.loads(response_register.data.decode())
            self.assertTrue(data_register['status'] == SUCCESS)
            self.assertTrue(
                data_register['message'] == REGISTER_SUCCESS
            )
            self.assertTrue(data_register['auth_token'])
            self.assertTrue(response_register.content_type == JSON_CONTENT_TYPE)
            self.assertTrue(response_register.status_code, 201)

            # user login
            response_login = self.client.post(
                '/auth/login',
                data=json.dumps(dict(
                    email=EMAIL,
                    password=PASSWORD
                )),
                content_type=JSON_CONTENT_TYPE,
            )
            data_login = json.loads(response_login.data.decode())
            self.assertTrue(data_login['status'] == SUCCESS)
            self.assertTrue(data_login['message'] == LOG_IN_SUCCESS)
            self.assertTrue(data_register['auth_token'])
            self.assertTrue(response_login.content_type == JSON_CONTENT_TYPE)
            self.assertEqual(response_login.status_code, 200)
            # blacklist a valid token
            blacklist_token = BlacklistToken(
                token=json.loads(response_login.data.decode())['auth_token'])
            db.session.add(blacklist_token)
            db.session.commit()
            # blacklisted valid token logout
            response_logout = self.client.post(
                '/auth/logout',
                headers=dict(
                    Authorization=f"Bearer {json.loads(response_login.data.decode())['auth_token']}"
                )
            )
            data = json.loads(response_logout.data.decode())
            self.assertTrue(data['status'] == FAIL)
            self.assertTrue(data['message'] == 'Token blacklisted. Please log in again.')
            self.assertEqual(response_logout.status_code, 401)

    def test_valid_blacklisted_token_user(self):
        """ 0009 Test for user status with a blacklisted valid token """
        with self.client:
            resp_register = register_user(self, username=USERNAME, email=EMAIL, password=PASSWORD)
            # blacklist a valid token
            blacklist_token = BlacklistToken(
                token=json.loads(resp_register.data.decode())['auth_token'])
            db.session.add(blacklist_token)
            db.session.commit()
            response = self.client.get(
                '/auth/status',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        resp_register.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Token blacklisted. Please log in again.')
            self.assertEqual(response.status_code, 401)

    def test_user_status_malformed_bearer_token(self):
        """ 0010 Test for user status with malformed bearer token"""
        with self.client:
            resp_register = register_user(self, EMAIL, EMAIL, PASSWORD)
            response = self.client.get(
                '/auth/status',
                headers=dict(
                    Authorization='Bearer' + json.loads(
                        resp_register.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == 'Bearer token malformed.')
            self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    unittest.main()
