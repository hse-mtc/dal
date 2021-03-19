# pylint: disable=ungrouped-imports

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
)

User = get_user_model()

# ------------------------------------------------------------------------------


class PopulateAPIView(GenericAPIView):
    serializer_class = PopulateSerializer
    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        # pylint: disable=too-many-locals

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

        # ----------------------------------------------------------------------
        # auth

        create_users()

        students, _ = Group.objects.get_or_create(name="students")
        teachers, _ = Group.objects.get_or_create(name="teachers")
        milfaculty_heads, _ = Group.objects.get_or_create(
            name="milfaculty_heads")
        content_type = ContentType.objects.get_for_model(Group)

        create_permissions(content_type)

        students.permissions.set(get_student_permissions())
        teachers.permissions.set(get_teacher_permissions())
        milfaculty_heads.permissions.set(get_milfaculty_head_permissions())

        students.user_set.add(User.objects.get(username="student"))
        teachers.user_set.add(User.objects.get(username="teacher"))
        milfaculty_heads.user_set.add(
            User.objects.get(username="milfaculty_head"))

        # ----------------------------------------------------------------------
        # common

        subjects = create_subjects()

        # ----------------------------------------------------------------------
        # dms

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
        create_favorite_books(books[:11], User.objects.get(username="vspelyak"))

        # ----------------------------------------------------------------------
        # lms

        faculties = create_faculties()
        programs = create_programs(faculties)

        milfaculties = create_milfaculties()
        milspecialties = create_milspecialties()
        milgroups = create_milgroups(milfaculties)

        return Response(status=status.HTTP_201_CREATED)
