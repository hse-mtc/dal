import request from '@/utils/request'

export function deleteDocument(params) {
  return request({
    url: '/delete_document',
    method: 'get',
    params
  })
}
