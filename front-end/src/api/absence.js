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
    url: '/lms/absence_journal/',
    method: 'get',
    params
  })
}

export function postAbsence(params) {
  return request({
    url: '/lms/absence/',
    method: 'post',
    data: {
      id: params.id,
      date: params.date,
      absenceType: params.absenceType,
      absenceStatus: params.absenceStatus,
      studentid: {
        id: params.studentid.id,
        name: params.studentid.name,
        surname: params.studentid.surname,
        patronymic: params.studentid.patronymic,
      },
      reason: params.reason,
      comment: params.comment
    }
  })
}

export function deleteAbsence(params) {
  return request({
    url: '/lms/absence/',
    method: 'delete',
    params
  })
}