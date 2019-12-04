import request from '@/utils/request'

export function getDocuments(params) {
  return request({
    url: '/documents',
    method: 'get',
    params
  })
}
