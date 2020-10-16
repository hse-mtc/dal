import request from '@/utils/request'

export function login(data) {
  return request({
    url: '/auth/tokens/obtain/',
    method: 'post',
    data
  })
}

export function getInfo(token) {
  return request({
    url: '/auth/users/info/',
    method: 'get',
  })
}

export function logout() {
  return request({
    url: '/auth/users/logout/',
    method: 'post'
  })
}
