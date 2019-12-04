import request from '@/utils/request'

export function getDocuments(authors ,published_places) {
  return request({
    url: '/documents',
    method: 'get',
    params : {authors: authors, publish_places: published_places}
  })
}
