import request from '@/utils/request';
import GetAuthHeader from '@/utils/auth';
import { stringify } from 'qs';


export async function query(params) {
  return request(`/api/roles?${stringify(params)}`, {
    headers: GetAuthHeader()
  });
}

export async function getPermissionTemplate() {
  return request('/api/roles/template', {
    headers: GetAuthHeader()
  });
}

export async function newRole(params) {
  return request('/api/roles', {
    method: 'POST',
    data: params,
    headers: GetAuthHeader()
  });
}

export async function editRole(params) {
  return request('/api/roles', {
    method: 'PUT',
    data: params,
    headers: GetAuthHeader()
  });
}

export async function getRoleWithPermissions(params) {
  return request('/api/roles/'+params.id, {
    headers: GetAuthHeader()
  });
}


