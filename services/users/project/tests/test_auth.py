# _*_ coding: utf-8 _*_
__author__ = 'taylor'
__date__ = '2019/4/15 11:32 PM'

import unittest

from project import db
from project.api.models import User
from project.tests.base import BaseTestCase
import json


class TestAuthBlueprint(BaseTestCase):

    def test_registration(self):
        """ Test for user registration"""
        with self.client:
            response = self.client.post(
                '/auth/register',
                data=json.dumps(dict(
                    username='grav007',
                    email='tay1@163.com',
                    password='123456'
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == '注册成功.')
            self.assertTrue(data['auth_token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)


if __name__ == '__main__':
    unittest.main()