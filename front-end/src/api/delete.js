import request from '@/utils/request'

export function deleteDocument(params) {
  return request({
    url: `/dms/documents/${params.id}`,
    method: 'delete',
  })
}
