import os

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

# ------------------------------------------------------------------------------
# Populate imports

# Common

from common.populate.subjects import create_subjects
from common.populate.milspecialties import create_milspecialties
from common.populate.prod_universities import (
    create_faculties,
    create_programs,
)

# Auth

from auth.models import Group
from auth.populate.permissions import (
    get_applicant_permissions,
    get_student_permissions,
    get_teacher_permissions,
    get_milfaculty_head_permissions,
)

# DMS

from dms.populate.common import (
    create_authors,
    create_publishers,
)
from dms.populate.papers import (
    create_categories,
)
from dms.populate.class_materials import (
    create_sections,
    create_topics,
)

# LMS

from lms.populate.uniforms import create_uniforms
from lms.populate.achievements import (
    create_achievement_types,
)
from lms.populate.common import (
    create_milfaculties,
    create_milgroups,
)
from lms.populate.lessons import (
    create_rooms,
)
from lms.populate.students import (
    create_skills,
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

        # ----------------------------------------------------------------------
        # Common

        print("Populating `common` models...", end="")

        milspecialties = create_milspecialties()
        subjects = create_subjects(milspecialties)
        faculties = create_faculties()
        create_programs(faculties)

        print(" OK")

        # ----------------------------------------------------------------------
        # DMS

        print("Populating `dms` models...", end="")

        create_authors()
        create_publishers()
        create_categories()

        sections = create_sections(subjects[0])
        create_topics(sections[0])

        print(" OK")

        # ----------------------------------------------------------------------
        # LMS

        print("Populating `lms` models...", end="")

        milfaculties = create_milfaculties()
        create_milgroups(milfaculties, milspecialties)

        create_skills()

        create_achievement_types()

        create_rooms()

        create_uniforms(milfaculties=milfaculties)

        print(" OK")
