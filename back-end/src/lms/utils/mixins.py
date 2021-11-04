from django.db.models import QuerySet

from rest_framework import status
from rest_framework import generics
from rest_framework import mixins

from rest_framework.response import Response

from auth.models import Permission

from lms.models.students import Student
from lms.models.teachers import Teacher

from lms.utils.functions import get_personnel_from_request_user
from lms.types.personnel import Personnel


class QuerySetScopingMixin(generics.GenericAPIView, mixins.CreateModelMixin):
    permission_allow_read_only = False
    scoped_permission_class = None

    # --------------------------------------------------------------------------
    # Scoping for getting the queryset.
    # Applies to GET (all or by id), PUT, PATCH and DELETE requests.

    def handle_scope_milfaculty(self, personnel: Personnel) -> QuerySet:
        # pylint: disable=unused-argument
        return self.queryset.none()

    def handle_scope_milgroup(self, personnel: Personnel) -> QuerySet:
        # pylint: disable=unused-argument
        return self.queryset.none()

    def handle_scope_self(self, personnel: Personnel) -> QuerySet:
        # pylint: disable=unused-argument
        return self.queryset.none()

    def get_queryset(self) -> QuerySet:
        """
        Filter queryset according to the scopes,
        specified in the user permission(s) related to the request.

        :return: filtered QuerySet
        """

        # pylint: disable=too-many-return-statements

        if self.request.user.is_superuser:
            return self.queryset

        if self.permission_allow_read_only:
            return self.queryset

        scope = self.request.user.get_perm_scope(
            self.scoped_permission_class.permission_class, self.request.method)

        if scope == Permission.Scope.ALL:
            return self.queryset

        personnel = get_personnel_from_request_user(self.request.user)

        # Empty queryset for the users that are not Personnel.
        if personnel is None:
            return self.queryset.none()

        personnel: Personnel

        if scope == Permission.Scope.MILFACULTY:
            return self.handle_scope_milfaculty(personnel)

        if scope == Permission.Scope.MILGROUP:
            return self.handle_scope_milgroup(personnel)

        if scope == Permission.Scope.SELF:
            return self.handle_scope_self(personnel)

        return self.queryset.none()

    # --------------------------------------------------------------------------
    # Scoping for creation.
    # Applies to POST requests.

    # pylint: disable=unused-argument
    def allow_scope_milfaculty_on_create(
        self,
        data: dict,
        personnel: Personnel,
    ) -> bool:
        return False

    # pylint: disable=unused-argument
    def allow_scope_milgroup_on_create(
        self,
        data: dict,
        personnel: Personnel,
    ) -> bool:
        return False

    # pylint: disable=unused-argument
    def allow_scope_self_on_create(
        self,
        data: dict,
        personnel: Personnel,
    ) -> bool:
        return False

    # pylint: disable=too-many-return-statements
    def is_creation_allowed_by_scope(
        self,
        data: dict,
    ) -> bool:
        if self.request.user.is_superuser:
            return True

        scope = self.request.user.get_perm_scope(
            self.scoped_permission_class.permission_class, self.request.method)

        if scope == Permission.Scope.ALL:
            return True

        personnel = get_personnel_from_request_user(self.request.user)

        # Not allowed for the users that are not Personnel.
        if personnel is None:
            return False

        personnel: Personnel

        if scope == Permission.Scope.MILFACULTY:
            return self.allow_scope_milfaculty_on_create(data, personnel)

        if scope == Permission.Scope.MILGROUP:
            return self.allow_scope_milgroup_on_create(data, personnel)

        if scope == Permission.Scope.SELF:
            return self.allow_scope_self_on_create(data, personnel)

        return False

    def create(
        self,
        request,
        *args,
        **kwargs,
    ) -> Response:
        """
        Create new model object with scope checks.
        """

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if self.is_creation_allowed_by_scope(request.data):
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED,
                            headers=headers)

        return Response(
            {"detail": "You do not have permission to perform this action."},
            status=status.HTTP_403_FORBIDDEN)


class StudentTeacherQuerySetScopingMixin(QuerySetScopingMixin):
    """
    Filters all students by milfaculty (except for the ALL scope)
    and teachers by scope.

    Requires presence of "student" and "teacher" fields.
    """

    def handle_scope_milfaculty(self, personnel: Personnel):
        assert (isinstance(personnel, Student) or
                isinstance(personnel, Teacher), "Unhandled Personnel type")

        return self.queryset.filter(
            student__milgroup__milfaculty=personnel.milfaculty,
            teacher__milfaculty=personnel.milfaculty,
        )

    def allow_scope_milfaculty_on_create(self, data, personnel: Personnel):
        assert (isinstance(personnel, Student) or
                isinstance(personnel, Teacher), "Unhandled Personnel type")

        student = Student.objects.filter(id=data["student"])
        teacher = Teacher.objects.filter(id=data["teacher"])

        if not student.exists() or not teacher.exists():
            return False

        student_matches = student.first().milfaculty == personnel.milfaculty
        teacher_matches = teacher.first().milfaculty == personnel.milfaculty

        return student_matches and teacher_matches

    def handle_scope_milgroup(self, personnel: Personnel):
        match personnel:
            case Student():
                return self.queryset.filter(
                    student__milgroup__milfaculty=personnel.milgroup.milfaculty,
                    teacher__milgroups__contains=personnel.milgroup,
                )
            case Teacher():
                return self.queryset.filter(
                    student__milgroup__milfaculty=personnel.milfaculty,
                    teacher__user=personnel.user,
                )
            case _:
                assert False, "Unhandled Personnel type"

    def allow_scope_milgroup_on_create(self, data, personnel: Personnel):
        student = Student.objects.filter(id=data["student"])
        teacher = Teacher.objects.filter(id=data["teacher"])

        if not student.exists() or not teacher.exists():
            return False

        student = student.first()
        teacher = teacher.first()

        match personnel:
            case Student():
                st_ch = personnel.milgroup == student.milgroup
                te_ch = personnel.milgroup in teacher.milgroups
                return st_ch and te_ch

            case Teacher():
                st_ch = student.milgroup in personnel.milgroups
                te_ch = teacher.user == personnel.user
                return st_ch and te_ch

            case _:
                assert False, "Unhandled Personnel type"

    def handle_scope_self(self, personnel: Personnel):
        match personnel:
            case Student():
                return self.queryset.filter(student=personnel)
            case Teacher():
                return self.queryset.filter(
                    teacher=personnel,
                    student__milgroup__milfaculty=personnel.milfaculty,
                )
            case _:
                assert False, "Unhandled Personnel type"

    def allow_scope_self_on_create(self, data, personnel: Personnel):
        match personnel:
            case Student():
                return False

            case Teacher():
                student = Student.objects.filter(id=data["student"])
                if not student.exists():
                    return False

                st_milfaculty = student.first().milfaculty
                milfaculty_check = st_milfaculty == personnel.milfaculty
                return data["teacher"] == personnel.id and milfaculty_check

            case _:
                assert False, "Unhandled Personnel type"
