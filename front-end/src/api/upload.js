import request from '@/utils/request'

export function uploadDocs(data) {
  return request({
    url: '/dms/documents/',
    method: 'post',
    headers: {
      'Content-Type': 'multipart/form-data'
    },
    data
  })
}
