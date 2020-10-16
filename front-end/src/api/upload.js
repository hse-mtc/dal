import request from '@/utils/request'

export function uploadDocs(data) {
  return request({
    url: '/dms/papers/',
    method: 'post',
    headers: {
      'Content-Type': 'multipart/form-data'
    },
    data
  })
}

export function updateDocs(data, id) {
  return request({
    url: `/dms/papers/${id}/`,
    method: 'patch',
    headers: {
      'Content-Type': 'multipart/form-data'
    },
    data
  })
}
