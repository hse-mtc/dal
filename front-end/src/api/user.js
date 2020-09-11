import request from '@/utils/request'

export function login(data) {
  return request({
    url: '/dms/user/login/',
    method: 'post',
    data
  })
}

export function getInfo(token) {
  return request({
    url: '/dms/user/info/',
    method: 'get',
    params: { token }
  })
}

export function logout() {
  return request({
    url: '/dms/user/logout/',
    method: 'post'
  })
}
