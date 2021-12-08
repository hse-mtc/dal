from django.contrib.auth import get_user_model

from ams.models.staff import Staff
from common.models.personal import ContactInfo, BirthInfo
from common.utils.populate import get_or_create

User = get_user_model()


def create_staffs(
    users: dict[str, User],
) -> dict[str, Staff]:
    staffs = [
        {
            "surname": "Жугина_0",
            "name": "Жугина",
            "patronymic": "Жугина",
            "user": users["zhugina@mail.com"],

            "post": Staff.Post.CLERK.value,

            "birth_info": {
                "date": "1995-06-23",
                "country": "Беларусь",
                "place": "Минск",
            },
            "contact_info": {
                "personal_phone_number": "70000000008",
            },
        }
    ]

    objects = {}

    for fields in staffs:
        fields["contact_info"] = get_or_create(
            ContactInfo,
            **fields.pop("contact_info"),
        )
        fields["birth_info"] = get_or_create(
            BirthInfo,
            **fields.pop("birth_info"),
        )

        object_ = get_or_create(Staff, **fields)

        object_.save()

        objects[fields["surname"]] = object_

    return objects
