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
    roles = Role.to_paged_dict(Role.query, current_page, page_size)
    return jsonify(roles), 200


@roles_blueprint.route('/roles', methods=['POST'])
def new_role():
    current_page = request.args.get('current_page', 1, type=int)
    page_size = min(request.args.get('page_size', BaseConfig.LIST_PER_PAGE, type=int), 100)
    roles = Role.to_paged_dict(Role.query, current_page, page_size)
    return jsonify(roles), 200


@roles_blueprint.route('/roles', methods=['PUT'])
def edit_role():
    current_page = request.args.get('current_page', 1, type=int)
    page_size = min(request.args.get('page_size', BaseConfig.LIST_PER_PAGE, type=int), 100)
    roles = Role.to_paged_dict(Role.query, current_page, page_size)
    return jsonify(roles), 200
