import request from '@/utils/request'

export function getAbsence(params) {
  return request({
    url: '/lms/absence/',
    method: 'get',
    params
  })
}

export function getAbsenceJournal(params) {
  return request({
    url: '/lms/absence-journal/',
    method: 'get',
    params
  })
}

export function patchAbsence(data) {
  if (data.studentid !== undefined)
    data.studentid = { id: data.studentid.id };
  return request({
    url: `/lms/absence/${data.id}`,
    method: 'patch',
    data
  })
}

export function deleteAbsence(params) {
  return request({
    url: `/lms/absence/${params.id}`,
    method: 'delete'
  })
}