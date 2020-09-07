import request from '@/utils/request'

export function getAuthors(params) {
  return request({
    url: '/authors/',
    method: 'get',
    params
  })
}
