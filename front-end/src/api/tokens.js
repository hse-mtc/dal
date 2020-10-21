import request from '@/utils/request'

export function updateAccess(data) {
  return request({
    url: '/auth/tokens/refresh/',
    method: 'post',
    data
  })
}

