import json
import unittest
import time
from datetime import datetime
import datetime as dt
from project.tests.base import BaseTestCase
from project.api.models import User, Post, Role
from project import db


def add_role(command):
    role = Role.new_role(command)
    db.session.add(role)
    db.session.commit()
    return role


class TestRoleService(BaseTestCase):
    """Tests for the Roles Service."""

    def test_add_role_with_permissions_ok(self):
        """0001_Ensure add role with permissions can be added to the database."""
        with self.client:
            response = self.client.post(
                '/api/roles',
                data=json.dumps({
                    'name': '角色test',
                    'desc': '角色desc',
                    'permissions': {
                        101: [1, 2, 3],
                        201: [0, 1, 4],
                    }
                }),
                content_type='application/json',
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 201)
            self.assertIn('新增角色成功', data['message'])
            self.assertIn('success', data['status'])
            roles_response = self.client.get('/api/roles')
            roles = json.loads(roles_response.data.decode())
            print("roles: ", roles)
            self.assertEqual(roles['list'], [{'id': 1, 'name': '角色test', 'desc': '角色desc'}])
            self.assertEqual(len(roles['list']), 1)
            self.assertEqual(roles['pagination']['current'], 1)

    def test_get_role_with_permissions_by_id(self):
        """0002_get role with permissions is ok."""
        command = {
            'name': '角色name',
            'desc': '角色desc',
            'permissions': {
                101: [1, 2, 3],
                201: [0, 1, 4],
            }
        }
        role = add_role(command);
        print("role: ", role.id)
        with self.client:
            response = self.client.get(f'/api/roles/{role.id}')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual('success', data['status'])
            print('roles_data: ', data)
            self.assertEqual(
                {
                    101: [1, 2, 3],
                    201: [0, 1, 4],
                }
                , data['data']['permissions'])


if __name__ == '__main__':
    unittest.main()
