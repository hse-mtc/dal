from datetime import (
    datetime,
    timedelta,
)

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

# ------------------------------------------------------------------------------
# Populate imports

from auth.models import Group
from auth.populate.users import create_users
from auth.populate.permissions import (
    get_student_permissions,
    get_teacher_permissions,
    get_milfaculty_head_permissions,
)

from common.populate.subjects import create_subjects

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

from lms.views.populate import (
    create_faculties,
    create_programs,
    create_milfaculties,
    create_milspecialties,
    create_milgroups,
    create_ranks,
    create_posts,
    create_passports,
    create_recruitments_offices,
    create_university_infos,
    create_students,
    create_teachers,
    create_absences,
    create_punishments,
    create_encouragements,
    create_achievement_types,
    create_achievements,
    create_subjects as create_lms_subjects,
    create_rooms,
    create_lessons,
    create_absence_restriction_time,
    create_marks,
    create_uniforms,
    create_student_posts,
    create_student_skills,
    create_contact_infos,
)

from lms.functions import get_date_range

# ------------------------------------------------------------------------------


class Command(BaseCommand):
    help = "Populate database with fake data (dev mode on;y)"

    def handle(self, *args, **options):
        # ----------------------------------------------------------------------
        # Auth

        User = get_user_model()

        create_users()

        students, _ = Group.objects.get_or_create(name="students")
        teachers, _ = Group.objects.get_or_create(name="teachers")
        milfaculty_heads, _ = Group.objects.get_or_create(
            name="milfaculty_heads")

        students.permissions.set(get_student_permissions())
        teachers.permissions.set(get_teacher_permissions())
        milfaculty_heads.permissions.set(get_milfaculty_head_permissions())

        students.user_set.add(User.objects.get(email="student@mail.com"))
        teachers.user_set.add(User.objects.get(email="teacher@mail.com"))
        milfaculty_heads.user_set.add(
            User.objects.get(email="milfaculty_head@mail.com"))

        # ----------------------------------------------------------------------
        # Common

        subjects = create_subjects()

        # ----------------------------------------------------------------------
        # DMS

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
        create_favorite_books(books[:11],
                              User.objects.get(email="vspelyak@mail.com"))

        # ----------------------------------------------------------------------
        # LMS

        faculties = create_faculties()
        programs = create_programs(faculties)

        milfaculties = create_milfaculties()
        milspecialties = create_milspecialties()
        milgroups = create_milgroups(milfaculties)

        ranks = create_ranks()
        posts = create_posts()

        # nearest day for 18XX milgroups
        nearest_day = datetime.strptime(
            get_date_range(datetime.now() - timedelta(6), datetime.now(),
                           4)[0], "%Y-%m-%d")

        passports = create_passports()
        offices = create_recruitments_offices()
        infos = create_university_infos(programs)
        student_posts = create_student_posts()
        student_skills = create_student_skills()
        contacts = create_contact_infos()
        students = create_students(
            milgroups,
            programs,
            milspecialties,
            passports,
            offices,
            infos,
            student_posts,
            student_skills,
            contacts,
        )

        teachers = create_teachers(milgroups, milfaculties, ranks, posts)

        create_absences(students, nearest_day)

        create_punishments(students, teachers, nearest_day)

        create_encouragements(students, teachers, nearest_day)

        achievement_types = create_achievement_types()
        create_achievements(achievement_types, students, nearest_day)

        subjects = create_lms_subjects()
        rooms = create_rooms()
        lessons = create_lessons(rooms, milgroups, subjects, nearest_day)

        create_absence_restriction_time()

        create_marks(lessons, students)

        create_uniforms(milfaculties)