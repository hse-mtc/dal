from django.core.management.base import BaseCommand

from django.contrib.auth import get_user_model

from auth.models import Group
from auth.populate.permissions import (
    get_applicant_permissions,
    get_student_permissions,
    get_teacher_permissions,
    get_milfaculty_head_permissions,
)


class Command(BaseCommand):
    help = "Populate database with prod data (for prod usage)"

    def handle(self, *args, **options):
        # ----------------------------------------------------------------------
        # Auth

        print("Populating `auth` models...", end="")

        applicants, _ = Group.objects.get_or_create(name="Абитуриент")
        students, _ = Group.objects.get_or_create(name="Студент")
        teachers, _ = Group.objects.get_or_create(name="Преподаватель")
        milfaculty_heads, _ = Group.objects.get_or_create(name="Начальник цикла")

        applicants.permissions.set(get_applicant_permissions())
        students.permissions.set(get_student_permissions())
        teachers.permissions.set(get_teacher_permissions())
        milfaculty_heads.permissions.set(get_milfaculty_head_permissions())

        print(" OK")
