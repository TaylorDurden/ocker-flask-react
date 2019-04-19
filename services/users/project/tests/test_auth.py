# _*_ coding: utf-8 _*_
__author__ = 'taylor'
__date__ = '2019/4/15 11:32 PM'

import unittest

from project import db
from project.api.models import User
from project.tests.base import BaseTestCase
import json


JSON_CONTENT_TYPE='application/json'


class TestAuthBlueprint(BaseTestCase):

    def test_registration(self):
        """ Test for user registration"""
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps(dict(
                    username='123456',
                    email='tay1@163.com',
                    password='123456'
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == '注册成功.')
            self.assertTrue(data['auth_token'])
            self.assertTrue(response.content_type == JSON_CONTENT_TYPE)
            self.assertEqual(response.status_code, 201)

    def test_registered_with_already_registered_user(self):
        """ Test registration with already registered email """
        user = User(
            username='123456',
            email='taylor@gmail.com',
        )
        db.session.add(user)
        db.session.commit()
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps(dict(
                    username='123456',
                    email='taylor@gmail.com',
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
        """ Test for login of registered-user login """
        with self.client:
            # user registration
            response_register = self.client.post(
                '/auth/register',
                data=json.dumps(dict(
                    username='taylor',
                    email='taylor@gmail.com',
                    password='123456'
                )),
                content_type=JSON_CONTENT_TYPE,
            )
            data_register = json.loads(response_register.data.decode())
            self.assertTrue(data_register['status'] == 'success')
            self.assertTrue(
                data_register['message'] == '注册成功.'
            )
            self.assertTrue(data_register['auth_token'])
            self.assertTrue(response_register.content_type == JSON_CONTENT_TYPE)
            self.assertEqual(response_register.status_code, 201)
            # registered user login
            response = self.client.post(
                '/auth/login',
                data=json.dumps(dict(
                    username='taylor',
                    email='taylor@gmail.com',
                    password='123456'
                )),
                content_type=JSON_CONTENT_TYPE
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == '登录成功.')
            self.assertTrue(data['auth_token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

    def test_non_registered_user_login(self):
        """ Test for login of non-registered user """
        with self.client:
            response = self.client.post(
                '/auth/login',
                data=json.dumps(dict(
                    username='123456',
                    email='taylor1@gmail.com',
                    password='123456'
                )),
                content_type=JSON_CONTENT_TYPE
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(data['message'] == '用户不存在.')
            self.assertTrue(response.content_type == JSON_CONTENT_TYPE)
            self.assertEqual(response.status_code, 404)

    def test_user_status(self):
        """ Test for  user status """
        with self.client:
            response_register = self.client.post(
                '/auth/register',
                data=json.dumps(dict(
                    username='taylor',
                    email='taylor@163.com',
                    password='123456'
                )),
                content_type=JSON_CONTENT_TYPE
            )
            response = self.client.get(
                '/auth/status',
                headers=dict(
                    Authorization='Bearer ' + json.loads(
                        response_register.data.decode()
                    )['auth_token']
                )
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['data'] is not None)
            self.assertTrue(data['data']['email'] == 'taylor@163.com')
            self.assertTrue(data['data']['active'] is 'true' or 'false')
            self.assertTrue(data['data']['created_date'] is not None)
            self.assertEqual(response.status_code, 200)



if __name__ == '__main__':
    unittest.main()