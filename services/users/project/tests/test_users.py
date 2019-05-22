# _*_ coding: utf-8 _*_

__author__ = 'taylor'
__date__ = '2019/3/17 3:44 AM'

# services/users/project/tests/test_users.py


import json
import unittest
import time
from datetime import datetime
import datetime as dt
from project.tests.base import BaseTestCase
from project.api.models import User, Post
from project import db


def add_user(username, email, role_ids=[]):
    command = {'username': username, 'email': email, 'role_ids': role_ids}
    user = User.add_user(command)
    db.session.add(user)
    db.session.commit()
    return user


def add_post(body, user_id):
    post = Post(body=body, user_id=user_id)
    db.session.add(post)
    db.session.commit()
    return post


class TestUserService(BaseTestCase):
    """Tests for the Users Service."""

    def test_users(self):
        """Ensure the /ping route behaves correctly."""
        response = self.client.get('/api/users/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
        self.assertIn('success', data['status'])

    def test_add_user(self):
        """Ensure a new user can be added to the database."""
        with self.client:
            response = self.client.post(
                '/api/users',
                data=json.dumps({
                    'username': 'michael',
                    'email': 'michael@mherman.org',
                    'password': "123456",
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('michael@mherman.org was added!', data['message'])
            self.assertIn('success', data['status'])

    def test_add_user_invalid_json(self):
        """Ensure error is thrown if the JSON object is empty."""
        with self.client:
            response = self.client.post(
                '/api/users',
                data=json.dumps({}),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_invalid_json_keys(self):
        """
        Ensure error is thrown if the JSON object does not have a username key.
        """
        with self.client:
            response = self.client.post(
                '/api/users',
                data=json.dumps({
                    'email': 'michael@mherman.org',
                    'password': '123456',
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('Invalid payload.', data['message'])
            self.assertIn('fail', data['status'])

    def test_add_user_duplicate_email(self):
        """Ensure error is thrown if the email already exists."""
        with self.client:
            self.client.post(
                '/api/users',
                data=json.dumps({
                    'username': 'michael',
                    'email': 'michael@mherman.org',
                    'password': "123456",
                }),
                content_type='application/json',
            )
            response = self.client.post(
                '/api/users',
                data=json.dumps({
                    'username': 'michael',
                    'email': 'michael@mherman.org',
                    'password': "123456",
                    'role_ids': [],
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn(
                'Sorry. That email already exists.', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_user(self):
        """Ensure get single user behaves correctly."""
        user = add_user('michael', 'michael@mherman.org')
        with self.client:
            response = self.client.get(f'/api/users/{user.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('michael', data['data']['username'])
            self.assertIn('michael@mherman.org', data['data']['email'])
            self.assertIn('success', data['status'])

    def test_single_user_no_id(self):
        """Ensure error is thrown if an id is not provided."""
        with self.client:
            response = self.client.get('/api/users/blah')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_single_user_incorrect_id(self):
        """Ensure error is thrown if the id does not exist."""
        with self.client:
            response = self.client.get('/api/users/999')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('User does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_all_users(self):
        """Ensure get all users behaves correctly."""
        add_user('michael', 'michael@mherman.org', )
        add_user('fletcher', 'fletcher@notreal.com', )
        with self.client:
            response = self.client.get('/api/users')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['list']), 2)
            self.assertIn('michael', data['list'][0]['username'])
            # self.assertIn(
            #     'michael@mherman.org', data['list'][0]['email'])
            self.assertIn('fletcher', data['list'][1]['username'])
            self.assertTrue(data['list'][1]['active'])

    def test_all_users_filter_by_last_edit_date_range(self):
        """Ensure get all users filter by last edit date and order by last edit date behaves correctly."""
        add_user('michael', 'michael@mherman.org')
        time.sleep(1)
        add_user('fletcher', 'fletcher@notreal.com')
        with self.client:
            # e.g 2019-04-30T16:09:38.998Z
            start_date_str = (datetime.now() - dt.timedelta(days=1)).isoformat() + 'Z'
            end_date_str = (datetime.now() + dt.timedelta(days=1)).isoformat() + 'Z'
            response = self.client.get(f'/api/users?last_edit_date%5B0%5D={start_date_str}'
                                       f'&last_edit_date%5B1%5D={end_date_str}'
                                       '&sort_by=last_edit_date&order=desc'
                                       '&active=true%2Cfalse')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['list']), 2)
            self.assertIn('michael', data['list'][1]['username'])
            # self.assertIn(
            #     'michael@mherman.org', data['list'][0]['email'])
            self.assertIn('fletcher', data['list'][0]['username'])
            self.assertTrue(data['list'][1]['active'])

    def test_all_users_filter_by_last_edit_date_range_order_by_post_count(self):
        """Ensure get all users order by post count behaves correctly."""
        mic = add_user('michael', 'michael@mherman.org')
        add_post('123test', mic.id)
        time.sleep(1)
        add_user('fletcher', 'fletcher@notreal.com')

        with self.client:
            # e.g 2019-04-30T16:09:38.998Z
            start_date_str = (datetime.now() - dt.timedelta(days=1)).isoformat() + 'Z'
            end_date_str = (datetime.now() + dt.timedelta(days=1)).isoformat() + 'Z'
            response = self.client.get(f'/api/users?last_edit_date%5B0%5D={start_date_str}'
                                       f'&last_edit_date%5B1%5D={end_date_str}'
                                       '&sort_by=post_count&order=desc'
                                       '&active=true%2Cfalse')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['list']), 2)
            self.assertEqual(1, data['list'][0]['post_count'])
            self.assertIn('michael', data['list'][0]['username'])
            # self.assertIn(
            #     'michael@mherman.org', data['list'][0]['email'])
            self.assertEqual(0, data['list'][1]['post_count'])
            self.assertIn('fletcher', data['list'][1]['username'])
            self.assertTrue(data['list'][1]['active'])

    def test_all_users_filter_by_last_edit_date_range_order_by_post_count(self):
        """Ensure get all users order by follower count behaves correctly."""
        mic = add_user('michael', 'michael@mherman.org')
        fle = add_user('fletcher', 'fletcher@notreal.com')
        mic.follow(fle)

        with self.client:
            # e.g 2019-04-30T16:09:38.998Z
            start_date_str = (datetime.now() - dt.timedelta(days=1)).isoformat() + 'Z'
            end_date_str = (datetime.now() + dt.timedelta(days=1)).isoformat() + 'Z'
            response = self.client.get('/api/users?sort_by=follower_count&order=desc')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['list']), 2)
            self.assertEqual(1, data['list'][0]['follower_count'])
            self.assertEqual(0, data['list'][0]['followed_count'])
            self.assertIn('fletcher', data['list'][0]['username'])
            # self.assertIn(
            #     'michael@mherman.org', data['list'][0]['email'])
            self.assertEqual(0, data['list'][1]['follower_count'])
            self.assertEqual(1, data['list'][1]['followed_count'])
            self.assertIn('michael', data['list'][1]['username'])
            self.assertTrue(data['list'][1]['active'])

    def test_main_no_users(self):
        """Ensure the main route behaves correctly when no users have been
        added to the database."""
        response = self.client.get('/api/users/index')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'All Users', response.data)
        self.assertIn(b'<p>No users!</p>', response.data)

    def test_main_with_users(self):
        """Ensure the main route behaves correctly when users have been
        added to the database."""
        add_user('michael', 'michael@mherman.org')
        add_user('fletcher', 'fletcher@notreal.com')
        with self.client:
            response = self.client.get('/api/users/index')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'All Users', response.data)
            self.assertNotIn(b'<p>No users!</p>', response.data)
            self.assertIn(b'michael', response.data)
            self.assertIn(b'fletcher', response.data)


if __name__ == '__main__':
    unittest.main()
