import request from '@/utils/request'

export function getExistingTags(params) {
  return request({
    url: '/dms/tags/',
    method: 'get',
    params
  }).then(response => {
      return response.data.map(tag => ({
          key: tag,
          value: tag,
      }))
  })
}
