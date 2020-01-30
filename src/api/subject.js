import request from '@/utils/request'

export function getSubject(params) {
  return request({
    url: '/subject',
    method: 'get',
    params
  })
}
