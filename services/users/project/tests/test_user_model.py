# _*_ coding: utf-8 _*_
__author__ = 'taylor'
__date__ = '2019/4/15 10:04 PM'

import unittest

from project import db
from project.api.models import User
from project.tests.base import BaseTestCase


def add_user(username, email):
    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()
    return user


class TestUserModel(BaseTestCase):

    def test_password_hashing(self):
        u = User(username='susan', email='1@1.com')
        u.set_password('cat')
        self.assertTrue(u.check_password('cat'))
        self.assertFalse(u.check_password('dog'))

    def test_follow(self):
        join = add_user(username='join', email='join@163.com')
        susan = add_user(username='susan', email='susan@163.com')
        self.assertEqual(join.followed.all(), [])
        self.assertEqual(join.followers.all(), [])

        join.follow(susan)
        db.session.commit()
        self.assertTrue(join.is_following(susan))
        self.assertTrue(join.followed.count(), 1)
        self.assertTrue(join.followed.first().username, 'susan')
        self.assertTrue(susan.followers.count(), 1)
        self.assertTrue(susan.followers.first().username, 'join')

        join.unfollow(susan)
        db.session.commit()
        self.assertFalse(join.is_following(susan))
        self.assertEqual(join.followed.count(), 0)
        self.assertEqual(susan.followers.count(), 0)

    def test_encode_auth_token(self):
        user = User(username='aaa', email='1@test.com')
        db.session.add(user)
        db.session.commit()
        auth_token = user.encode_auth_token(user.id)
        print(f'auth_token:{auth_token}')
        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self):
        user = User(
            username='aaa',
            email='test@test.com',
        )
        db.session.add(user)
        db.session.commit()
        auth_token = user.encode_auth_token(user.id)
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertTrue(User.decode_auth_token(auth_token) == user.id)


if __name__ == '__main__':
    unittest.main()
