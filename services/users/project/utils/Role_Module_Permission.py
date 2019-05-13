from enum import Enum, unique


@unique
class Module(Enum):
    用户管理 = 101
    角色管理 = 201


@unique
class Permission(Enum):
    查看 = 0
    新增 = 1
    编辑 = 2
    删除 = 3
    启用 = 4
    禁用 = 5


class PermissionGroup(object):
    name = ""
    module_permissions = []

    def __init__(self, name, module_permissions):
        self.name = name
        self.module_permissions = module_permissions

    def to_dict(self):
        return {
            'module_permissions': [x.to_dict() for x in self.module_permissions],
            'name': self.name
        }


class ModulePermission(object):
    module = {}
    permissions = []

    def __init__(self, module, permissions):
        self.module = module
        self.permissions = permissions

    def to_dict(self):
        return {
            'module_name': self.module.name,
            'module': self.module.value,
            'permissions': [{'name': x.name, 'value': x.value} for x in self.permissions]
        }


class PermissionGroupList(object):
    __module_group_permission_map = []

    def __init__(self):
        self.__module_group_permission_map = [
            PermissionGroup(name="用户中心", module_permissions=[
                ModulePermission(Module.用户管理, [Permission.查看, Permission.新增, Permission.编辑, Permission.启用, Permission.禁用])
            ]),
            PermissionGroup(name="系统设置", module_permissions=[
                ModulePermission(Module.角色管理, [Permission.查看, Permission.新增, Permission.编辑])
            ])
        ]

    def get_permissions(self):
        return self.__module_group_permission_map

    def to_dict(self):
        return {
            'items': [x.to_dict() for x in self.__module_group_permission_map]
        }

    # def get_permissions_tree(self):
    #     tree = [ for item in self.__module_group_permission_map]


class RolesMixin(object):
    @staticmethod
    def to_collection_dict(resources):
        data = {
            'list': [item.to_dict() for item in resources],
        }
        return data
