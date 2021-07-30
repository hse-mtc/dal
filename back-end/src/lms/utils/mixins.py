from django.db.models import QuerySet

from rest_framework import status
from rest_framework.response import Response

from lms.models.students import Student
from lms.models.teachers import Teacher
from lms.utils.functions import get_user_from_request

from auth.models import Permission, User


class QuerySetScopingMixin:

    scoped_permission_class = None

    # Scoping for getting the queryset
    # (applies to GET (all or by id),
    # PUT, PATCH AND DELETE)

    # pylint: disable=unused-argument
    def handle_scope_milfaculty(self, user_type: str, user: User) -> QuerySet:
        return self.queryset.none()

    # pylint: disable=unused-argument
    def handle_scope_milgroup(self, user_type: str, user: User) -> QuerySet:
        return self.queryset.none()

    # pylint: disable=unused-argument
    def handle_scope_self(self, user_type: str, user: User) -> QuerySet:
        return self.queryset.none()

    # pylint: disable=too-many-return-statements
    def get_queryset(self) -> QuerySet:
        """
        Filter queryset according to the scopes,
        specified in the user permission(s) related to the request.

        :return: filtered QuerySet
        """
        if self.request.user.is_superuser:
            return self.queryset

        scope = self.request.user.get_perm_scope(
            self.scoped_permission_class.permission_class, self.request.method)

        if scope == Permission.Scope.ALL:
            return self.queryset

        # check if user is a teacher ot a student
        user_type, user = get_user_from_request(self.request.user)
        if user is None:
            # return nothing if user is not a student or a teacher
            return self.queryset.none()

        if scope == Permission.Scope.MILFACULTY:
            return self.handle_scope_milfaculty(user_type, user)

        if scope == Permission.Scope.MILGROUP:
            return self.handle_scope_milgroup(user_type, user)

        if scope == Permission.Scope.SELF:
            return self.handle_scope_self(user_type, user)

        return self.queryset.none()

    # Scoping for creation
    # (applies to POST)

    # pylint: disable=unused-argument
    def allow_scope_milfaculty_on_create(self, data: dict, user_type: str,
                                         user: User) -> bool:
        return False

    # pylint: disable=unused-argument
    def allow_scope_milgroup_on_create(self, data: dict, user_type: str,
                                       user: User) -> bool:
        return False

    # pylint: disable=unused-argument
    def allow_scope_self_on_create(self, data: dict, user_type: str,
                                   user: User) -> bool:
        return False

    # pylint: disable=too-many-return-statements
    def is_creation_allowed_by_scope(self, data: dict) -> bool:
        if self.request.user.is_superuser:
            return True

        scope = self.request.user.get_perm_scope(
            self.scoped_permission_class.permission_class, self.request.method)

        if scope == Permission.Scope.ALL:
            return True

        # check if user is a teacher ot a student
        user_type, user = get_user_from_request(self.request.user)
        if user is None:
            # return False if user is not a student or a teacher
            return False

        if scope == Permission.Scope.MILFACULTY:
            return self.allow_scope_milfaculty_on_create(data, user_type, user)

        if scope == Permission.Scope.MILGROUP:
            return self.allow_scope_milgroup_on_create(data, user_type, user)

        if scope == Permission.Scope.SELF:
            return self.allow_scope_self_on_create(data, user_type, user)

        return False

    def create(self, request, *args, **kwargs) -> Response:
        """
        Create new model object with scope checks.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # check scoping
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

    def handle_scope_milfaculty(self, user_type, user):
        if user_type == "student":
            return self.queryset.filter(
                student__milgroup__milfaculty=user.milgroup.milfaculty,
                teacher__milfaculty=user.milgroup.milfaculty,
            )
        if user_type == "teacher":
            return self.queryset.filter(
                student__milgroup__milfaculty=user.milfaculty,
                teacher__milfaculty=user.milfaculty,
            )
        return self.queryset.none()

    def allow_scope_milfaculty_on_create(self, data, user_type, user):
        student = Student.objects.filter(id=data["student"])
        teacher = Teacher.objects.filter(id=data["teacher"])

        if (not student.exists()) or (not teacher.exists()):
            return False

        if user_type == "student":
            user_milfaculty = user.milgroup.milfaculty
        elif user_type == "teacher":
            user_milfaculty = user.milfaculty
        else:
            return False

        student = student.first()
        teacher = teacher.first()
        st_ch = user_milfaculty == student.milgroup.milfaculty
        te_ch = user_milfaculty == teacher.milfaculty
        return st_ch and te_ch

    def handle_scope_milgroup(self, user_type, user):
        if user_type == "student":
            return self.queryset.filter(
                student__milgroup__milfaculty=user.milgroup.milfaculty,
                teacher__milgroups__contains=user.milgroup,
            )
        if user_type == "teacher":
            return self.queryset.filter(
                student__milgroup__milfaculty=user.milfaculty,
                teacher__user=user,
            )
        return self.queryset.none()

    def allow_scope_milgroup_on_create(self, data, user_type, user):
        student = Student.objects.filter(id=data["student"])
        teacher = Teacher.objects.filter(id=data["teacher"])

        if (not student.exists()) or (not teacher.exists()):
            return False

        student = student.first()
        teacher = teacher.first()

        # pylint: disable=no-else-return
        if user_type == "student":
            st_ch = user.milgroup == student.milgroup
            te_ch = user.milgroup in teacher.milgroups
            return st_ch and te_ch
        elif user_type == "teacher":
            st_ch = student.milgroup in user.milgroups
            te_ch = teacher.user == user
            return st_ch and te_ch
        return False

    def handle_scope_self(self, user_type, user):
        if user_type == "student":
            return self.queryset.filter(student=user)
        if user_type == "teacher":
            return self.queryset.filter(
                teacher=user,
                student__milgroup__milfaculty=user.milfaculty,
            )
        return self.queryset.none()

    def allow_scope_self_on_create(self, data, user_type, user):
        if user_type == "teacher":
            student = Student.objects.filter(id=data["student"])
            if not student.exists():
                return False

            st_milfaculty = student.first().milgroup.milfaculty
            milfaculty_check = st_milfaculty == user.milfaculty
            return (data["teacher"] == user.id) and milfaculty_check
        return False
