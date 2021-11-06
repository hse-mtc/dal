# pylint: disable=invalid-name,too-many-statements

from datetime import (
    datetime,
    timedelta,
)

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

# ------------------------------------------------------------------------------
# Populate imports

# Common

from common.populate.subjects import create_subjects
from common.populate.milspecialties import create_milspecialties
from common.populate.universities import (
    create_faculties,
    create_programs,
)

from common.utils.date import get_date_range

# Auth

from auth.models import Group
from auth.populate.users import create_users
from auth.populate.permissions import (
    get_student_permissions,
    get_teacher_permissions,
    get_milfaculty_head_permissions,
)

# AMS

from ams.populate.applicants import create_applicants

# DMS

from dms.populate.documents import create_files
from dms.populate.common import (
    create_authors,
    create_publishers,
)
from dms.populate.papers import (
    create_categories,
    create_papers,
)
from dms.populate.class_materials import (
    create_sections,
    create_topics,
    create_class_materials,
)
from dms.populate.books import (
    create_books,
    create_favorite_books,
)

# LMS

from lms.populate.encouragements import create_encouragements
from lms.populate.marks import create_marks
from lms.populate.punishments import create_punishments
from lms.populate.teachers import create_teachers
from lms.populate.uniforms import create_uniforms
from lms.populate.absences import (
    create_absences,
    create_absence_restriction_time,
)
from lms.populate.achievements import (
    create_achievement_types,
    create_achievements,
)
from lms.populate.common import (
    create_milfaculties,
    create_milgroups,
)
from lms.populate.lessons import (
    create_rooms,
    create_lessons,
)
from lms.populate.students import (
    create_students,
    create_skills,
)


# ------------------------------------------------------------------------------


class Command(BaseCommand):
    help = "Populate database with fake data (dev mode only)"

    def handle(self, *args, **options):
        # ----------------------------------------------------------------------
        # Auth

        print("Populating `auth` models...", end="")

        User = get_user_model()

        users = create_users()

        students, _ = Group.objects.get_or_create(name="Студент")
        teachers, _ = Group.objects.get_or_create(name="Преподаватель")
        milfaculty_heads, _ = Group.objects.get_or_create(
            name="Начальник цикла")

        students.permissions.set(get_student_permissions())
        teachers.permissions.set(get_teacher_permissions())
        milfaculty_heads.permissions.set(get_milfaculty_head_permissions())

        students.user_set.add(User.objects.get(email="gakhromov@mail.com"))
        students.user_set.add(User.objects.get(email="askatsevalov@mail.com"))
        students.user_set.add(User.objects.get(email="veisakov@mail.com"))
        students.user_set.add(User.objects.get(email="naaliev@mail.com"))
        students.user_set.add(User.objects.get(email="avkurkin@mail.com"))
        students.user_set.add(User.objects.get(email="psivanov@mail.com"))

        teachers.user_set.add(User.objects.get(email="ivnikandrov@mail.com"))
        teachers.user_set.add(User.objects.get(email="ivmesheryakov@mail.com"))
        teachers.user_set.add(User.objects.get(email="ivkovalchuk@mail.com"))
        teachers.user_set.add(User.objects.get(email="ksgavrilov@mail.com"))

        milfaculty_heads.user_set.add(
            User.objects.get(email="dnrepalov@mail.com"))

        print(" OK")

        # ----------------------------------------------------------------------
        # Common

        print("Populating `common` models...", end="")

        subjects = create_subjects()
        milspecialties = create_milspecialties()
        faculties = create_faculties()
        programs = create_programs(faculties)

        print(" OK")

        # ----------------------------------------------------------------------
        # AMS

        print("Populating `ams` models...", end="")

        applicants = create_applicants(
            programs=programs,
            milspecialties=milspecialties,
        )

        print(" OK")

        # ----------------------------------------------------------------------
        # DMS

        print("Populating `dms` models...", end="")

        files = create_files()

        authors = create_authors()
        publishers = create_publishers()

        categories = create_categories()
        create_papers(
            authors=authors,
            categories=categories,
            publishers=publishers,
            files=files,
        )

        sections = create_sections(subjects[0])
        topics = create_topics(sections[0])
        create_class_materials(
            files=files,
            topics=topics,
        )

        books = create_books(
            authors=authors,
            files=files,
            publishers=publishers,
            subjects=subjects,
        )
        create_favorite_books(
            books[:11],
            User.objects.get(email="dnrepalov@mail.com"),
        )

        print(" OK")

        # ----------------------------------------------------------------------
        # LMS

        print("Populating `lms` models...", end="")

        milfaculties = create_milfaculties()
        milgroups = create_milgroups(milfaculties)

        # nearest day for 18XX milgroups
        nearest_day = datetime.strptime(
            get_date_range(datetime.now() - timedelta(6), datetime.now(), 4)[0],
            "%Y-%m-%d",
        )

        skills = create_skills()
        students = create_students(
            users=users,
            milgroups=milgroups,
            skills=skills,
            programs=programs,
        )

        teachers = create_teachers(
            milgroups=milgroups,
            milfaculties=milfaculties,
            users=users,
        )

        create_absence_restriction_time()
        create_absences(
            students=students,
            nearest_day=nearest_day,
        )

        create_punishments(
            students=students,
            teachers=teachers,
            nearest_day=nearest_day,
        )

        create_encouragements(
            students=students,
            teachers=teachers,
            nearest_day=nearest_day,
        )

        achievement_types = create_achievement_types()
        create_achievements(
            achievement_types=achievement_types,
            students=students,
            nearest_day=nearest_day,
        )

        rooms = create_rooms()
        lessons = create_lessons(
            subjects=subjects,
            rooms=rooms,
            milgroups=milgroups,
            teachers=teachers,
            nearest_day=nearest_day,
        )

        create_marks(
            lessons=lessons,
            students=students,
        )

        create_uniforms(milfaculties=milfaculties)

        print(" OK")
