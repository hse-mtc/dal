from collections import namedtuple

from django.contrib.auth import get_user_model

from auth.models import Profile

User = get_user_model()

Data = namedtuple(
    "Data",
    [
        "email",
        "password",
        "is_staff",
        "is_superuser",
        "surname",
        "name",
        "patronymic",
    ],
)


def create_user(data: Data) -> (User, Profile):
    query = User.objects.filter(email=data.email)

    if not query.exists():
        User.objects.create_user(
            email=data.email,
            password=data.password,
            is_staff=data.is_staff,
            is_superuser=data.is_superuser,
        )

    user = query.first()

    profile, _ = Profile.objects.get_or_create(
        surname=data.surname,
        name=data.name,
        patronymic=data.patronymic,
        user=user,
    )

    return user, profile


def create_users() -> list[(User, Profile)]:
    users = [
        Data(
            email="vspelyak@mail.com",
            password="qwerty",
            is_staff=True,
            is_superuser=True,
            surname="Пеляк",
            name="Виктор",
            patronymic="Степанович",
        ),
        Data(
            email="test@mail.com",
            password="qwerty",
            is_staff=True,
            is_superuser=False,
            surname="Фамилия",
            name="Имя",
            patronymic="Отчество",
        ),
        Data(
            email="student@mail.com",
            password="qwerty",
            is_staff=True,
            is_superuser=False,
            surname="Студентов",
            name="Студент",
            patronymic="Студентов",
        ),
        Data(
            email="teacher@mail.com",
            password="qwerty",
            is_staff=True,
            is_superuser=False,
            surname="Преподов",
            name="Препод",
            patronymic="Преподович",
        ),
        Data(
            email="milfaculty_head@mail.com",
            password="qwerty",
            is_staff=True,
            is_superuser=False,
            surname="Начальников",
            name="Начальник",
            patronymic="Начальникович",
        ),
    ]

    return [create_user(data) for data in users]
