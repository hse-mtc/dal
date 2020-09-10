import request from '@/utils/request'

export function getAuthors(params) {
  return request({
    url: '/dms/authors/',
    method: 'get',
    params
  })
}
