import request from '@/utils/request'

export function getPublishPlaces(params) {
  return request({
    url: '/dms/publishers/',
    method: 'get',
    params
  })
}
