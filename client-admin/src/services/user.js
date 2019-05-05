import request from '@/utils/request';
import GetAuthHeader from '@/utils/auth';
import { stringify } from 'qs';


export async function query(params) {
  return request(`/api/users?${stringify(params)}`, {
    headers: GetAuthHeader()
  });
}

export async function queryCurrent() {
  return request('/api/auth/status', {
    headers: GetAuthHeader()
  });
}

export async function register() {
  return request('/auth/register');
}
