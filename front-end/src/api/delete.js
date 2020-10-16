import request from '@/utils/request'

export function deleteDocument(params) {
  return request({
    url: `/dms/papers/${params.id}/`,
    method: 'delete',
  })
}
