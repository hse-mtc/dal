# pylint: disable=ungrouped-imports
from datetime import (
    datetime,
    timedelta,
)

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType

from rest_framework import status

from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny

from common.serializers.populate import PopulateSerializer

# ------------------------------------------------------------------------------
# Populate imports

from auth.populate.users import create_users
from auth.populate.permissions import (
    create_permissions,
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
)

from lms.functions import get_date_range

User = get_user_model()

# ------------------------------------------------------------------------------


class PopulateAPIView(GenericAPIView):
    serializer_class = PopulateSerializer
    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        # pylint: disable=too-many-locals,unused-variable,too-many-statements

        # ----------------------------------------------------------------------
        # Validate request

        serializer: PopulateSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        apps = serializer.validated_data

        if apps["dms"] and not (apps["auth"] and apps["common"]):
            detail = "Can not populate `dms` without `auth` and `common`."
            return Response(
                data={"detail": detail},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if apps["lms"] and not (apps["auth"] and apps["common"]):
            detail = "Can not populate `lms` without `auth` and `common`."
            return Response(
                data={"detail": detail},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # ----------------------------------------------------------------------
        # auth
        if apps["auth"]:
            users = create_users()

            students, _ = Group.objects.get_or_create(name="students")
            teachers, _ = Group.objects.get_or_create(name="teachers")
            milfaculty_heads, _ = Group.objects.get_or_create(
                name="milfaculty_heads")
            content_type = ContentType.objects.get_for_model(Group)

            create_permissions(content_type)

            students.permissions.set(get_student_permissions())
            teachers.permissions.set(get_teacher_permissions())
            milfaculty_heads.permissions.set(get_milfaculty_head_permissions())

            students.user_set.add(User.objects.get(email="student@mail.com"))
            teachers.user_set.add(User.objects.get(email="teacher@mail.com"))
            milfaculty_heads.user_set.add(
                User.objects.get(email="milfaculty_head@mail.com"))

        # ----------------------------------------------------------------------
        # common
        if apps["common"]:
            subjects = create_subjects()

        # ----------------------------------------------------------------------
        # dms
        if apps["dms"]:
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
        # lms
        if apps["lms"]:
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
            students = create_students(
                milgroups,
                programs,
                milspecialties,
                passports,
                offices,
                infos,
                users
            )

            teachers = create_teachers(milgroups, milfaculties, ranks, posts, users)

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

        return Response(status=status.HTTP_201_CREATED)
