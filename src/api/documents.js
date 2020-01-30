import request from '@/utils/request'

export function getDocuments(authors, published_places, start_date, end_date, text) {
  return request({
    url: '/articles',
    method: 'get',
    params : {authors: authors, publish_places: published_places, start_date: start_date, end_date: end_date, text: text}
  })
}