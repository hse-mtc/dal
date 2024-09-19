from django.core.mail import send_mail
from django.contrib.auth import get_user_model

from rest_framework import pagination, viewsets
from rest_framework import permissions
from rest_framework import status
from rest_framework import mixins

from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from django_filters.rest_framework import DjangoFilterBackend

from drf_spectacular.views import extend_schema

from common.constants import MUTATE_ACTIONS
from common.email.registration import send_regconf_email
from common.serializers.personal import check_email_exists

from common.views.choices import GenericChoicesList

from auth.models import Group, Permission
from auth.permissions import BasePermission
from auth.tokens.registration import generate_regconf_token

from lms.models.teachers import Teacher
from lms.models.common import Milgroup
from lms.models.students import (
    Student,
    Note,
)

from lms.serializers.students import (
    StudentSerializer,
    StudentMutateSerializer,
    NoteSerializer,
    ApproveStudentMutateSerializer,
    ApproveStudentSerializer,
)

from lms.filters.students import (
    StudentFilter,
    NoteFilter,
)

from lms.utils.mixins import QuerySetScopingMixin

from lms.types.personnel import Personnel

from common.models.personal import ContactInfo, PersonalDocumentsInfo


class StudentPermission(BasePermission):
    permission_class = "students"
    view_name_rus = "Студенты"
    # Student creation via POST is not allowed,
    # as it is handled by the applicant's form procedures.
    methods = ["get", "put", "patch", "delete"]
    scopes = [
        Permission.Scope.ALL,
        Permission.Scope.MILFACULTY,
        Permission.Scope.MILGROUP,
        Permission.Scope.SELF,
    ]


class ActivatePermission(BasePermission):
    permission_class = "activate-students"
    view_name_rus = "Подтверждение регистрации"
    methods = ["get", "put", "patch"]
    scopes = [
        Permission.Scope.ALL,
        Permission.Scope.MILFACULTY,
        Permission.Scope.MILGROUP,
    ]


class StudentNotePermission(BasePermission):
    permission_class = "student-notes"
    view_name_rus = "Заметки о студентах"
    scopes = [
        Permission.Scope.SELF,
    ]


class StudentPageNumberPagination(pagination.PageNumberPagination):
    page_size_query_param = "page_size"


@extend_schema(tags=["students"])
class StudentViewSet(QuerySetScopingMixin, ModelViewSet):
    # pylint: disable=too-many-public-methods
    queryset = Student.objects.order_by("surname", "name", "patronymic", "id")

    permission_classes = [StudentPermission]
    scoped_permission_class = StudentPermission

    filter_backends = [DjangoFilterBackend, SearchFilter]

    filterset_class = StudentFilter
    search_fields = ["surname", "name", "patronymic"]

    pagination_class = StudentPageNumberPagination

    def get_serializer_class(self):
        mutate_actions = MUTATE_ACTIONS + [
            "registration",
            "registration_for_existing_students",
            "register_from_applicant",
        ]
        if self.action in mutate_actions:
            return StudentMutateSerializer
        return StudentSerializer

    def handle_scope_milfaculty(self, personnel: Personnel):
        match personnel:
            case Student() | Teacher():
                milfaculty = personnel.milfaculty
            case _:
                assert False, "Unhandled Personnel type"

        return self.queryset.filter(milgroup__milfaculty=milfaculty)

    def handle_scope_milgroup(self, personnel: Personnel):
        match personnel:
            case Student():
                return self.queryset.filter(milgroup=personnel.milgroup)
            case Teacher():
                return self.queryset.filter(milgroup__in=personnel.milgroups)
            case _:
                assert False, "Unhandled Personnel type"

    def handle_scope_self(self, personnel: Personnel):
        match personnel:
            case Student():
                return self.queryset.filter(user=personnel.user)
            case Teacher():
                return self.queryset.none()
            case _:
                assert False, "Unhandled Personnel type"

    @action(detail=False, methods=["patch"], permission_classes=[permissions.AllowAny])
    def registration(self, request):
        user_ = get_user_model()

        email = request.data["email"]
        user = user_.objects.create_user(
            email=email,
            password=user_.objects.make_random_password(),
        )

        instance = Student.objects.filter(contact_info__corporate_email=email).first()
        instance.milgroup = Milgroup.objects.get(pk=request.data["milgroup"])
        instance.user = user
        instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(
        detail=False, methods=["post"], permission_classes=[permissions.IsAuthenticated]
    )
    def register_from_applicant(self, request):
        request.data[
            "status"
        ] = "ST"  # Выставляем входной структуре статус обучающегося
        serializer = self.get_serializer_class()(
            data=request.data
        )  # TODO: write new serializer
        serializer.is_valid(raise_exception=True)

        corporate_email = serializer.validated_data["contact_info"]["corporate_email"]
        user = serializer.validated_data["user"]

        contact_info = ContactInfo.objects.get(corporate_email=corporate_email)

        student = serializer.save()

        student.user = user
        student.contact_info = contact_info

        # Если студент регистрировался в 2022 или 2023 году, у него нет ИНН и СНИЛСа в системе,
        # нужно заполнить
        if student.personal_documents_info == None:
            student.personal_documents_info = PersonalDocumentsInfo(
                tax_id="", insurance_number=""
            )

        student.save()

        students, _ = Group.objects.get_or_create(name="Студент")
        students.user_set.add(user)

        applicants, _ = Group.objects.get_or_create(name="Абитуриент")
        applicants.user_set.remove(user)

        return Response(self.get_serializer(student).data)

    @registration.mapping.post
    def registration_for_existing_students(self, request):
        request.data["status"] = "ST"
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["contact_info"]["corporate_email"]

        if check_email_exists(email):
            return Response(
                {"error_message": "email_already_exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        student = serializer.save()

        user = get_user_model().objects.create_user(
            email=email,
            password=get_user_model().objects.make_random_password(),
            campuses=["MO"],
            is_active=False,
        )

        student.user = user
        student.save()

        return Response(self.get_serializer(student).data)


@extend_schema(tags=["students"])
class ActivateStudentViewSet(QuerySetScopingMixin, ModelViewSet):
    queryset = Student.objects.all()

    permission_classes = [ActivatePermission]
    scoped_permission_class = ActivatePermission

    filter_backends = [DjangoFilterBackend]
    filterset_class = StudentFilter
    serializer_class = StudentSerializer

    def handle_scope_milfaculty(self, personnel: Personnel):
        match personnel:
            case Student() | Teacher():
                milfaculty = personnel.milfaculty
            case _:
                assert False, "Unhandled Personnel type"

        return self.queryset.filter(milgroup__milfaculty=milfaculty)

    def handle_scope_milgroup(self, personnel: Personnel):
        match personnel:
            case Student():
                return self.queryset.filter(milgroup=personnel.milgroup)
            case Teacher():
                return self.queryset.filter(milgroup__in=personnel.milgroups)
            case _:
                assert False, "Unhandled Personnel type"

    # TODO(TmLev): Revisit.
    def list(self, request: Request, *args, **kwargs) -> Response:
        queryset = self.get_queryset().filter(
            status__in=[
                Student.Status.ENROLLED,
            ]
        )

        user = request.user

        if hasattr(user, "teacher"):
            queryset = queryset.filter(milgroup__in=user.teacher.milgroups.all())
        if hasattr(user, "student"):
            queryset = queryset.filter(milgroup=user.student.milgroup)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_update(self, serializer):
        return serializer.save()

    # TODO(TmLev): Revisit.
    def update(self, request: Request, *args, **kwargs) -> Response:
        student = self.get_object()

        if student.user is None:
            return Response(
                data={
                    "detail": "Student has no user and must register first",
                },
                status=status.HTTP_428_PRECONDITION_REQUIRED,
            )

        old_status = student.status

        serializer = self.get_serializer(
            student,
            data=request.data,
            partial=kwargs.pop("partial", False),
        )
        serializer.is_valid(raise_exception=True)
        student: Student = self.perform_update(serializer)

        new_status = student.status

        match old_status, new_status:
            case Student.Status.ENROLLED.value, Student.Status.STUDYING.value:
                raise NotImplementedError("shrug")

        if getattr(student, "_prefetched_objects_cache", None):
            # If "prefetch_related" has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            # pylint: disable=protected-access
            student._prefetched_objects_cache = {}

        return Response(serializer.data)


# TODO(TmLev): send email, link should forward to front end app.
def confirm_student_registration(
    email: str,
    token: str,
) -> None:
    link = f"localhost:9528/change-password?token={str(token)}"
    print(link)

    html_message = f"""
        <p>Здравствуйте!</p>\n
        <p>Вы зарегистрировались в системе Даль ВУЦ ВШЭ.</p>\n
        <p>Ссылка для задания пароля: {link}</p>\n
    """

    print("Sending reg mail")
    send_mail(
        subject="Подтверждение регистрации в системе Даль",
        message=None,  # Send `html_message`.
        from_email=None,  # Django will use `DEFAULT_FROM_EMAIL`.
        recipient_list=[email],
        html_message=html_message,
    )


@extend_schema(tags=["students"])
class NoteViewSet(ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

    permission_classes = [StudentNotePermission]
    scoped_permission_class = StudentNotePermission

    filter_backends = [DjangoFilterBackend]
    filterset_class = NoteFilter

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)
        if self.request.user.is_superuser:
            return queryset

        scope = self.request.user.get_perm_scope(
            self.scoped_permission_class.permission_class, self.request.method
        )

        if scope == Permission.Scope.SELF:
            return queryset

        return queryset.none()

    # no need to check on create as user id is automatically
    # received from the request by the serializer


@extend_schema(tags=["students", "choices"])
class StudentStatusChoicesList(GenericChoicesList):
    choices_class = Student.Status


@extend_schema(tags=["students", "choices"])
class StudentPostChoicesList(GenericChoicesList):
    choices_class = Student.Post


class ApproveStudentPermission(BasePermission):
    permission_class = "approve-student"
    viewset = "approve-student"
    view_name_rus = "Подтверждение регистрации студентов"
    methods = ["get", "patch"]
    scopes = [
        Permission.Scope.ALL,
        Permission.Scope.SELF,
        Permission.Scope.MILFACULTY,
        Permission.Scope.MILGROUP,
    ]


@extend_schema(tags=["students"])
class ApproveStudentViewSet(
    QuerySetScopingMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Student.objects.filter(
        user__isnull=False,
        user__is_active=False,
    )

    permission_classes = [ApproveStudentPermission]
    scoped_permission_class = ApproveStudentPermission

    filter_backends = [DjangoFilterBackend]
    filterset_class = StudentFilter

    def get_serializer_class(self):
        if self.action in MUTATE_ACTIONS:
            return ApproveStudentMutateSerializer
        return ApproveStudentSerializer

    def partial_update(self, request: Request, *args, **kwargs) -> Response:
        print("Getting form")
        student = self.get_object()
        serializer = self.get_serializer(student, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(student, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            student._prefetched_objects_cache = {}

        send_regconf_email(
            address=student.fullname,
            email=student.user.email,
            url=request.META["HTTP_REFERER"],
            token=generate_regconf_token(student.user),
        )

        return Response()

    def perform_update(self, serializer):
        serializer.save()

    def handle_scope_milfaculty(self, personnel: Personnel):
        match personnel:
            case Student():
                return self.queryset.filter(
                    milgroup__milfaculty=personnel.milgroup.milfaculty
                )
            case Teacher():
                print(f"QS: {self.queryset}")
                print(f"MF: {personnel.milfaculty}")
                return self.queryset.filter(milgroup__milfaculty=personnel.milfaculty)
            case _:
                assert False, "Unhandled Personnel type"

    def handle_scope_milgroup(self, personnel: Personnel):
        match personnel:
            case Student():
                return self.queryset.filter(milgroup=personnel.milgroup)
            case Teacher():
                return self.queryset.filter(milgroup=personnel.milgroup)
            case _:
                assert False, "Unhandled Personnel type"
