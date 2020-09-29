import request from '@/utils/request'

export function getPaperCategories(params) {
  return request({
    url: '/dms/categories/',
    method: 'get',
    params
  })
}

export function addPaperCategories(params) {
  return request({
    url: '/dms/categories/',
    method: 'post',
    data: {title: params}
  })
}

export function deletePaperCategories(params) {
  return request({
    url: `/dms/categories/${params.id}/`,
    method: 'delete'
  })
}
