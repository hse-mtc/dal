import request from '@/utils/request'

export function getEducationalMaterials(params) {
  return request({
    url: '/educational_materials',
    method: 'get',
    params
  })
}
