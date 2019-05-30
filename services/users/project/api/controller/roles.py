from flask import Blueprint, jsonify, request, render_template, json
from project.api.models import User, Role
from project import db
from sqlalchemy import exc, and_, text, func
from project.config import BaseConfig
from datetime import datetime
from operator import itemgetter, attrgetter
from project.utils.Role_Module_Permission import PermissionGroupList
from project.resource.roles_resource import PermissionGroupListResource

roles_blueprint = Blueprint('roles', __name__)


@roles_blueprint.route('/roles/template', methods=['GET'])
def template():
    tree = PermissionGroupList().to_dict()
    # resource = PermissionGroupListResource(tree).to_dict()
    print(json.dumps(tree))
    return jsonify(tree), 200


@roles_blueprint.route('/roles', methods=['GET'])
def role_page_list():
    current_page = request.args.get('current_page', 1, type=int)
    page_size = min(request.args.get('page_size', BaseConfig.LIST_PER_PAGE, type=int), 100)

    roles = Role.to_paged_dict(Role.query, current_page, page_size, include_fields=False)
    print('roles: ', roles)
    return jsonify(roles)


@roles_blueprint.route('/roles-select', methods=['GET'])
def role_select_list():
    roles = Role.query.all()
    res = [x.to_dict(include_permissions=False) for x in roles]
    return jsonify(res)


@roles_blueprint.route('/roles/<role_id>', methods=['GET'])
def get_role_by(role_id):
    """Get single user details"""
    response_object = {
        'status': 'fail',
        'message': '角色不存在'
    }
    try:
        print("role_id: ", role_id)
        print("role_id_type: ", type(role_id))
        role = Role.query.filter_by(id=int(role_id)).first()
        print("role: ", role)
        if not role:
            return jsonify(response_object), 404
        else:
            response_object = {
                'status': 'success',
                'data': role.to_dict()
            }
            return jsonify(response_object), 200
    except Exception:
        raise


@roles_blueprint.route('/roles', methods=['POST'])
def new_role():
    post_data = request.get_json()
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }
    if not post_data:
        return jsonify(response_object), 400

    role_name = post_data.get('name')
    role_desc = post_data.get('desc')
    permissions = post_data.get('permissions')
    try:
        if role_name and role_desc and permissions:
            role = Role.new_role({'name': role_name, 'desc': role_desc, 'permissions': permissions})
            db.session.add(role)
            db.session.commit()
            response_object['status'] = 'success'
            response_object['message'] = '新增角色成功'
            return jsonify(response_object), 201
        else:
            response_object['message'] = '参数不合法'
            return jsonify(response_object), 400
    except exc.IntegrityError:
        db.session.rollback()
        return jsonify(response_object), 400


@roles_blueprint.route('/roles', methods=['PUT'])
def edit_role():
    post_data = request.get_json()
    response_object = {
        'status': 'fail',
        'message': '角色不存在'
    }
    command = {
        'id': post_data.get('id'),
        'name': post_data.get('name'),
        'desc': post_data.get('desc'),
        'permissions': post_data.get('permissions')
    }
    try:
        role = Role.query.filter_by(id=int(command['id'])).first()
        print("role: ", role)
        if not role:
            return jsonify(response_object), 404
        else:
            response_object = {
                'status': 'success',
            }
            role.edit(command)
            db.session.commit()
            return jsonify(response_object)
    except Exception:
        db.session.rollback()
        raise
