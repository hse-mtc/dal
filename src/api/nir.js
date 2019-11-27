import request from '@/utils/request'

export function nir(params) {
  return request({
    url: '/nir',
    method: 'get',
    params
  })
}
