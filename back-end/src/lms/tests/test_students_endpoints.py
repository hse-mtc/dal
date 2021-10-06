from operator import itemgetter

import pytest


@pytest.mark.django_db
def test_get_students_returns_list(su_client, student_data,
                                   assert_student_equals):
    # pylint: disable=too-many-locals

    count = 3
    for _ in range(count):
        data = student_data()

    response = su_client.get('/api/lms/students/')
    assert response.status_code == 200
    assert len(response.data) == count

    id_getter = itemgetter('id')
    response.data.sort(key=id_getter)
    min_id = min(response.data, key=id_getter)['id']

    for id_, student in enumerate(response.data, start=min_id):
        assert_student_equals(local_student_id=id_,
                              local_student=data,
                              remote_student=student)
