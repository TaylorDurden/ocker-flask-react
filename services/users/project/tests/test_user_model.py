# _*_ coding: utf-8 _*_
__author__ = 'taylor'
__date__ = '2019/4/15 10:04 PM'

import unittest

from project import db
from project.api.models import User, Role
from project.tests.base import BaseTestCase


def add_user(username, email):
    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()
    return user


def add_user_with_roles(command):
    user = User.add_user(command)
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

        join.un_follow(susan)
        db.session.commit()
        self.assertFalse(join.is_following(susan))
        self.assertEqual(join.followed.count(), 0)
        self.assertEqual(susan.followers.count(), 0)

    def test_encode_auth_token(self):
        user = User(username='aaa', email='1@test.com')
        db.session.add(user)
        db.session.commit()
        auth_token = user.encode_auth_token()
        print(f'auth_token:{auth_token}')
        self.assertTrue(isinstance(auth_token, bytes))

    def test_decode_auth_token(self):
        user = User(
            username='aaa',
            email='test@test.com',
        )
        db.session.add(user)
        db.session.commit()
        auth_token = user.encode_auth_token()
        self.assertTrue(isinstance(auth_token, bytes))
        self.assertTrue(User.decode_auth_token(auth_token) == user.id)
        self.assertTrue(User.decode_auth_token(
            auth_token.decode("utf-8")) == 1)

    def test_add_user_with_roles(self):
        role = Role.new_role({'name': 'test_role', 'desc': 'test_role_desc', 'permissions': {}})
        db.session.add(role)
        db.session.commit()
        command = {'username': 'a1', 'email': 'a1@163.com', 'role_ids': [role.id]}
        user = add_user_with_roles(command)
        db.session.add(user)
        db.session.commit()
        self.assertEqual(len(user.roles.all()), 1)
        self.assertEqual(user.roles[0].name, "test_role")

    def test_edit_user_with_roles(self):
        role = Role.new_role({'name': 'test_role', 'desc': 'test_role_desc', 'permissions': {}})
        role1 = Role.new_role({'name': 'test_role1', 'desc': 'test_role_desc1', 'permissions': {}})
        db.session.add(role)
        db.session.add(role1)
        db.session.commit()
        command = {'username': 'a1', 'email': 'a1@163.com', 'role_ids': [role.id]}
        user = add_user_with_roles(command)
        db.session.add(user)
        db.session.commit()
        print("user.roles1: ", user.roles.all())
        self.assertEqual(len(user.roles.all()), 1)
        command = {
            'id': user.id,
            'username': 'a12',
            'email': 'a12@163.com',
            'role_ids': [role.id, role1.id]
        }
        print("user.roles2 not edited: ", user.roles.all())
        [print("user.roles2 not edited: ", x.name) for x in user.roles.all()]
        user.edit_user(command)
        print("user.roles2: ", user.roles.all())
        [print("user.roles2 edited: ", x.name) for x in user.roles.all()]
        db.session.commit()
        self.assertEqual(len(user.roles.all()), 2)
        command = {
            'id': user.id,
            'username': 'a12',
            'email': 'a12@163.com',
            'role_ids': [role1.id]
        }
        print("user.roles3 not edited: ", user.roles.all())
        [print("user.roles3 not edited: ", x.name) for x in user.roles.all()]
        user.edit_user(command)
        print("user.roles3: ", user.roles.all())
        [print("user.roles3 edited: ", x.name) for x in user.roles.all()]
        db.session.commit()
        self.assertEqual(len(user.roles.all()), 1)


if __name__ == '__main__':
    unittest.main()
