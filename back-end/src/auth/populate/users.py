from collections import namedtuple

from django.contrib.auth import get_user_model

from conf.settings import TGBOT_EMAIL, TGBOT_PASSWORD

User = get_user_model()

Data = namedtuple(
    "Data",
    [
        "email",
        "password",
        "is_staff",
        "is_superuser",
    ],
)


def create_user(data: Data) -> User:
    query = User.objects.filter(email=data.email)

    if not query.exists():
        User.objects.create_user(
            email=data.email,
            password=data.password,
            is_staff=data.is_staff,
            is_superuser=data.is_superuser,
        )

    user = query.first()

    return user


def create_users() -> dict[str, User]:
    users = [
        Data(
            email="superuser@mail.com",
            password="qwerty",
            is_staff=True,
            is_superuser=True,
        ),
        # TODO (@gakhromov): remove superuser from
        # tgbot user and add appropriate permissions
        Data(
            email=TGBOT_EMAIL,
            password=TGBOT_PASSWORD,
            is_staff=True,
            is_superuser=True,
        ),
        Data(
            email="gakhromov@mail.com",
            password="qwerty",
            is_staff=True,
            is_superuser=False,
        ),
        Data(
            email="askatsevalov@mail.com",
            password="qwerty",
            is_staff=True,
            is_superuser=False,
        ),
        Data(
            email="veisakov@mail.com",
            password="qwerty",
            is_staff=True,
            is_superuser=False,
        ),
        Data(
            email="naaliev@mail.com",
            password="qwerty",
            is_staff=True,
            is_superuser=False,
        ),
        Data(
            email="avkurkin@mail.com",
            password="qwerty",
            is_staff=True,
            is_superuser=False,
        ),
        Data(
            email="psivanov@mail.com",
            password="qwerty",
            is_staff=True,
            is_superuser=False,
        ),
        Data(
            email="ivnikandrov@mail.com",
            password="qwerty",
            is_staff=True,
            is_superuser=False,
        ),
        Data(
            email="dnrepalov@mail.com",
            password="qwerty",
            is_staff=True,
            is_superuser=False,
        ),
        Data(
            email="ivmesheryakov@mail.com",
            password="qwerty",
            is_staff=True,
            is_superuser=False,
        ),
        Data(
            email="ivkovalchuk@mail.com",
            password="qwerty",
            is_staff=True,
            is_superuser=False,
        ),
        Data(
            email="ksgavrilov@mail.com",
            password="qwerty",
            is_staff=True,
            is_superuser=False,
        ),
    ]

    return {data.email: create_user(data) for data in users}
