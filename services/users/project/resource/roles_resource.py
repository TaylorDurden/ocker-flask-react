from project.utils.Role_Module_Permission import PermissionGroup


class PermissionGroupListResource(object):
    items = []

    def __init__(self, permission_groups):
        self.items = permission_groups

    def to_dict(self):
        return {
            'items': [x.to_dict() for x in self.items]
        }


class PermissionGroupResource(object):
    name = ''
    module_permissions = []

    def __init__(self, group):
        self.name = group.name
        self.module_permissions = [x.to_dict() for x in group.module_permissions]

    def to_dict(self):
        return {
            'name': self.name,
            'module_permissions': self.module_permissions
        }


class ModulePermissionResource(object):
    module_name = ''
    module = 0
    permissions = []

    def __init__(self, module_permission):
        self.module = module_permission.module.value
        self.module_name = module_permission.module.name
        self.permissions = [x.to_dict() for x in module_permission.permissions]

    def to_dict(self):
        return {
            'module_name': self.module_name,
            'module': self.module,
            'permissions': self.permissions
        }


class PermissionResource(object):
    name = ''
    value = ''

    def __init__(self, name, value):
        self.name = name
        self.value = value

    def to_dict(self):
        return {
            'name': self.name,
            'value': self.value
        }
