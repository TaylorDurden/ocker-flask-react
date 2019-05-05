import request from '@/utils/request';
import GetAuthHeader from '@/utils/auth';



export async function query(params) {
  return request(`/api/users?${stringify(params)}`);
}

export async function queryCurrent() {
  return request('/api/auth/status', {
    headers: GetAuthHeader()
  });
}

export async function register() {
  return request('/auth/register');
}
