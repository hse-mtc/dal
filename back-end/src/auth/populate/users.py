from collections import namedtuple

from django.contrib.auth import get_user_model

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


def create_users() -> list[User]:
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
            email="isakov@mail.com",
            password="qwerty",
            is_staff=True,
            is_superuser=False,
            surname="Исаков",
            name="Владислав",
            patronymic="Евгеньевич",
        ),
        Data(
            email="khromov@mail.com",
            password="qwerty",
            is_staff=True,
            is_superuser=False,
            surname="Хромов",
            name="Григорий",
            patronymic="Александрович",
        ),
        Data(
            email="kats@mail.com",
            password="qwerty",
            is_staff=True,
            is_superuser=False,
            surname="Кацевалов",
            name="Артем",
            patronymic="Сергеевич",
        ),
        Data(
            email="aliev@mail.com",
            password="qwerty",
            is_staff=True,
            is_superuser=False,
            surname="Алиев",
            name="Насир",
            patronymic="Ашурович",
        ),
        Data(
            email="kurkin@mail.com",
            password="qwerty",
            is_staff=True,
            is_superuser=False,
            surname="Куркин",
            name="Андрей",
            patronymic="Витальевич",
        ),
        Data(
            email="ivanov@mail.com",
            password="qwerty",
            is_staff=True,
            is_superuser=False,
            surname="Иванов",
            name="Петр",
            patronymic="Сидорович",
        ),
        Data(
            email="chuckmarikadze@mail.com",
            password="qwerty",
            is_staff=True,
            is_superuser=False,
            surname="Чукмарикадзе",
            name="Губарибек",
            patronymic="Алкинбеков",
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
            email="repalov@mail.com",
            password="qwerty",
            is_staff=True,
            is_superuser=False,
            surname="Репалов",
            name="Дмитрий",
            patronymic="Николаевич",
        ),
        Data(
            email="nikandrov@mail.com",
            password="qwerty",
            is_staff=True,
            is_superuser=False,
            surname="Никандров",
            name="Игорь",
            patronymic="Владимирович",
        ),
        Data(
            email="mesheryakov@mail.com",
            password="qwerty",
            is_staff=True,
            is_superuser=False,
            surname="Мещеряков",
            name="Иван",
            patronymic="Владимирович",
        ),
        Data(
            email="kovalchuk@mail.com",
            password="qwerty",
            is_staff=True,
            is_superuser=False,
            surname="Ковальчук",
            name="Иван",
            patronymic="Валентинович",
        ),
        Data(
            email="gavrilov@mail.com",
            password="qwerty",
            is_staff=True,
            is_superuser=False,
            surname="Гаврилов",
            name="Климент",
            patronymic="Сергеевич",
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

    users_data = {}

    for data in users:
        user = create_user(data)
        users_data[data.email] = user

    return users_data
