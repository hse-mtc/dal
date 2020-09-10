import request from '@/utils/request'

export function uploadDocs(data) {
  return request({
    url: '/dms/upload/',
    method: 'post',
    headers: {
      'Content-Type': 'multipart/form-data'
    },
    data
  })
}
