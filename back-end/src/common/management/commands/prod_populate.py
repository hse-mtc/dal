import os

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from auth.models import Group
from auth.populate.permissions import (
    get_applicant_permissions,
    get_student_permissions,
    get_teacher_permissions,
    get_milfaculty_head_permissions,
)

from common.populate.milspecialties import create_milspecialties
from common.populate.prod_universities import (
    create_faculties,
    create_programs,
)

User = get_user_model()


class Command(BaseCommand):
    help = "Populate database with prod data (for prod usage)"

    def handle(self, *args, **options):
        # ----------------------------------------------------------------------
        # Auth

        print("\nCreating superuser...", end="")
        superuser_email = os.environ.get("SUPERUSER_EMAIL")
        superuser_password = os.environ.get("SUPERUSER_PASSWORD")
        User.objects.get_or_create(
            email=superuser_email,
            defaults={
                "is_staff": True,
                "is_superuser": True,
            },
        )
        admin_user = User.objects.get(email=superuser_email)
        admin_user.set_password(superuser_password)
        admin_user.save()

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
