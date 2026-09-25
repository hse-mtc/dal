import pytest

from django.contrib.auth import get_user_model
from django.core.management import call_command
from rest_framework.test import APIClient

from auth.models import Group, Permission
from common.models.personal import ContactInfo
from lms.models.absences import Absence
from lms.models.common import Milfaculty, Milgroup
from lms.models.formations import FormationReport, FormationRemark
from lms.models.students import Student
from lms.models.teachers import Teacher


@pytest.fixture
def formation_people(db):
    faculty = Milfaculty.objects.create(title="Цикл 1", abbreviation="Ц1")
    other_faculty = Milfaculty.objects.create(title="Цикл 2", abbreviation="Ц2")
    group = Milgroup.objects.create(title="101", weekday=0, milfaculty=faculty)
    other_group = Milgroup.objects.create(
        title="201", weekday=0, milfaculty=other_faculty
    )

    def student(email, milgroup, post=None):
        user = get_user_model().objects.create_user(email=email, password="test")
        person = Student.objects.create(
            surname=email.split("@")[0],
            name="Иван",
            status=Student.Status.STUDYING,
            user=user,
            milgroup=milgroup,
            post=post,
            contact_info=ContactInfo.objects.create(),
        )
        return person

    commander = student("commander@test.ru", group, Student.Post.MILGROUP_COMMANDER)
    own_student = student("cadet@test.ru", group)
    other_student = student("other@test.ru", other_group)
    head_user = get_user_model().objects.create_user(
        email="head@test.ru", password="test"
    )
    Teacher.objects.create(
        surname="Начальник",
        name="Цикла",
        rank=Teacher.Rank.MAJOR,
        post=Teacher.Post.MILFACULTY_HEAD,
        milfaculty=faculty,
        user=head_user,
    )
    head_role = Group.objects.create(name="Начальник цикла")
    for viewset, methods in (
        ("formation-reports", ("get", "post", "patch")),
        ("formation-remarks", ("get", "post", "patch", "delete")),
    ):
        for method in methods:
            head_role.permissions.add(
                Permission.objects.create(
                    viewset=viewset,
                    method=method,
                    scope=Permission.Scope.MILFACULTY,
                    name=f"{viewset} {method}",
                )
            )
    head_user.groups.add(head_role)
    return commander, own_student, other_student, head_user, group, other_group


def report_data(group):
    return {
        "milgroup": group.id,
        "date": "2026-09-25",
        "roster_count": 10,
        "present_count": 6,
        "excused_count": 2,
        "unexcused_count": 1,
        "unknown_count": 1,
        "comment": "",
    }


@pytest.mark.django_db
def test_commander_submits_only_own_group_and_counts_are_consistent(formation_people):
    commander, _, _, _, group, other_group = formation_people
    client = APIClient()
    client.force_authenticate(user=commander.user)

    invalid = report_data(group)
    invalid["present_count"] = 7
    assert client.post("/api/lms/formation-reports/", invalid).status_code == 400

    response = client.post("/api/lms/formation-reports/", report_data(group))
    assert response.status_code == 201
    assert response.data["absent_count"] == 4
    assert response.data["created_by"] == commander.user_id
    assert Absence.objects.count() == 0
    assert (
        client.post("/api/lms/formation-reports/", report_data(group)).status_code
        == 400
    )
    assert (
        client.post("/api/lms/formation-reports/", report_data(other_group)).status_code
        == 403
    )

    reports = client.get("/api/lms/formation-reports/")
    assert reports.status_code == 200
    assert len(reports.data) == 1
    assert reports.data[0]["milgroup"] == group.id
    assert client.post("/api/lms/formation-remarks/", {}).status_code == 403


@pytest.mark.django_db
def test_cycle_head_corrects_counts_and_records_only_own_students(formation_people):
    _, own_student, other_student, head_user, group, other_group = formation_people
    own = FormationReport.objects.create(
        milgroup=group,
        roster_count=10,
        present_count=6,
        excused_count=2,
        unexcused_count=1,
        unknown_count=1,
        date="2026-09-25",
    )
    foreign = FormationReport.objects.create(
        milgroup=other_group,
        roster_count=1,
        present_count=1,
        excused_count=0,
        unexcused_count=0,
        unknown_count=0,
        date="2026-09-25",
    )
    client = APIClient()
    client.force_authenticate(user=head_user)

    reports = client.get("/api/lms/formation-reports/?date=2026-09-25")
    assert reports.status_code == 200
    assert [report["id"] for report in reports.data] == [own.id]
    corrected = client.patch(
        f"/api/lms/formation-reports/{own.id}/",
        {"present_count": 7, "unknown_count": 0},
    )
    assert corrected.status_code == 200
    assert corrected.data["updated_by"] == head_user.id
    assert (
        client.patch(
            f"/api/lms/formation-reports/{foreign.id}/", {"comment": "чужой"}
        ).status_code
        == 404
    )

    remark = client.post(
        "/api/lms/formation-remarks/",
        {
            "report": own.id,
            "student": own_student.id,
            "category": FormationRemark.Category.HAIRCUT,
            "comment": "",
        },
    )
    assert remark.status_code == 201
    assert remark.data["student_name"] == own_student.fullname
    assert (
        client.post(
            "/api/lms/formation-remarks/",
            {
                "report": own.id,
                "student": other_student.id,
                "category": FormationRemark.Category.HAIRCUT,
            },
        ).status_code
        == 400
    )
    assert (
        client.post(
            "/api/lms/formation-remarks/",
            {
                "report": foreign.id,
                "student": other_student.id,
                "category": FormationRemark.Category.HAIRCUT,
            },
        ).status_code
        == 403
    )

    detail = client.get(f"/api/lms/formation-reports/{own.id}/")
    assert [item["id"] for item in detail.data["remarks"]] == [remark.data["id"]]


@pytest.mark.django_db
def test_role_and_current_post_both_limit_access(formation_people):
    commander, own_student, _, head_user, group, _ = formation_people
    report = FormationReport.objects.create(
        milgroup=group,
        roster_count=1,
        present_count=1,
        excused_count=0,
        unexcused_count=0,
        unknown_count=0,
        date="2026-09-25",
    )
    client = APIClient()
    client.force_authenticate(user=own_student.user)
    assert client.get("/api/lms/formation-reports/").status_code == 403

    commander.post = None
    commander.save()
    client.force_authenticate(user=commander.user)
    assert client.get("/api/lms/formation-reports/").status_code == 403

    head_user.groups.clear()
    client.force_authenticate(user=head_user)
    assert client.get(f"/api/lms/formation-reports/{report.id}/").status_code == 403


@pytest.mark.django_db
def test_former_commander_cannot_access_formation_reports(formation_people):
    commander, _, _, _, group, _ = formation_people
    client = APIClient()
    client.force_authenticate(user=commander.user)
    Student.objects.filter(pk=commander.pk).update(status=Student.Status.EXPELLED)
    client.force_authenticate(user=get_user_model().objects.get(pk=commander.user_id))

    assert client.get("/api/lms/formation-reports/").status_code == 403
    assert (
        client.post("/api/lms/formation-reports/", report_data(group)).status_code
        == 403
    )


@pytest.mark.django_db
def test_commander_report_does_not_expose_head_remarks(formation_people):
    commander, own_student, _, head_user, group, _ = formation_people
    report = FormationReport.objects.create(
        milgroup=group,
        roster_count=1,
        present_count=1,
        excused_count=0,
        unexcused_count=0,
        unknown_count=0,
        date="2026-09-25",
    )
    FormationRemark.objects.create(
        report=report,
        student=own_student,
        student_name=own_student.fullname,
        category=FormationRemark.Category.HAIRCUT,
    )
    client = APIClient()
    client.force_authenticate(user=commander.user)
    response = client.get(f"/api/lms/formation-reports/{report.id}/")
    assert response.status_code == 200
    assert response.data["remarks"] == []

    client.force_authenticate(user=head_user)
    response = client.get(f"/api/lms/formation-reports/{report.id}/")
    assert len(response.data["remarks"]) == 1


@pytest.mark.django_db
def test_permission_registration_does_not_restore_revoked_head_access():
    head_role = Group.objects.create(name="Начальник цикла")
    call_command("register_permissions")
    permission = Permission.objects.get(
        viewset="formation-reports",
        method="get",
        scope=Permission.Scope.MILFACULTY,
    )
    assert head_role.permissions.filter(pk=permission.pk).exists()
    head_role.permissions.remove(permission)

    call_command("register_permissions")
    assert not head_role.permissions.filter(pk=permission.pk).exists()


@pytest.mark.django_db
def test_teacher_milgroup_scope_uses_assigned_groups(formation_people):
    _, _, _, _, group, other_group = formation_people
    user = get_user_model().objects.create_user(
        email="teacher@test.ru", password="test"
    )
    teacher = Teacher.objects.create(
        surname="Преподаватель",
        name="Группы",
        rank=Teacher.Rank.MAJOR,
        post=Teacher.Post.TEACHERS,
        milfaculty=group.milfaculty,
        user=user,
    )
    teacher.milgroups.add(group)
    for method in ("get", "post"):
        user.permissions.add(
            Permission.objects.create(
                viewset="formation-reports",
                method=method,
                scope=Permission.Scope.MILGROUP,
                name=f"formation-reports {method} group",
            )
        )
    own = FormationReport.objects.create(
        milgroup=group,
        roster_count=1,
        present_count=1,
        excused_count=0,
        unexcused_count=0,
        unknown_count=0,
        date="2026-09-24",
    )
    FormationReport.objects.create(
        milgroup=other_group,
        roster_count=1,
        present_count=1,
        excused_count=0,
        unexcused_count=0,
        unknown_count=0,
        date="2026-09-24",
    )
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.get("/api/lms/formation-reports/?date=2026-09-24")
    assert response.status_code == 200
    assert [item["id"] for item in response.data] == [own.id]
    assert (
        client.post("/api/lms/formation-reports/", report_data(group)).status_code
        == 201
    )
    assert (
        client.post("/api/lms/formation-reports/", report_data(other_group)).status_code
        == 403
    )


@pytest.mark.django_db
def test_roster_count_suggestion_counts_current_students_with_group_scope(
    formation_people,
):
    commander, own_student, _, head_user, group, other_group = formation_people
    Student.objects.filter(pk=own_student.pk).update(status=Student.Status.ENROLLED)
    for status in (Student.Status.EXPELLED, Student.Status.GRADUATED):
        Student.objects.create(
            surname=status,
            name="Иван",
            status=status,
            milgroup=group,
            contact_info=ContactInfo.objects.create(),
        )
    empty_group = Milgroup.objects.create(
        title="102", weekday=0, milfaculty=group.milfaculty
    )
    client = APIClient()
    client.force_authenticate(user=commander.user)
    url = "/api/lms/formation-reports/roster-count/"
    response = client.get(url, {"milgroup": group.id})
    assert response.status_code == 200
    assert response.data == {"count": 2}
    assert client.get(url, {"milgroup": other_group.id}).status_code == 403

    client.force_authenticate(user=head_user)
    assert client.get(url, {"milgroup": group.id}).data == {"count": 2}
    assert client.get(url, {"milgroup": empty_group.id}).data == {"count": 0}
    assert client.get(url, {"milgroup": other_group.id}).status_code == 403
