from django.contrib.auth import get_user_model
from django.db import models

from common.models.personal import Photo, BirthInfo, ContactInfo
from common.models.universities import Campus


class Staff(models.Model):

    # --------------------------------------------------------------------------

    class Post(models.TextChoices):
        CLERK = "Clerk", "Делопроизводитель"

    # --------------------------------------------------------------------------
    # Frequently accessed data.

    surname = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
    patronymic = models.CharField(
        max_length=64,
        blank=True,
    )
    user = models.OneToOneField(
        to=get_user_model(),
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    # --------------------------------------------------------------------------
    # Rarely accessed studying data.

    post = models.CharField(
        max_length=2,
        choices=Post.choices,
        default=Post.CLERK.value,
    )

    # --------------------------------------------------------------------------
    # Rarely accessed personal data.

    photo = models.OneToOneField(
        to=Photo,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    birth_info = models.OneToOneField(
        to=BirthInfo,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    contact_info = models.OneToOneField(
        to=ContactInfo,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    campus = models.CharField(
        choices=Campus.choices,
        max_length=2,
    )

    class Meta:
        verbose_name = "Staff"
        verbose_name_plural = "Staffs"

    def __str__(self):
        return f"[{self.id}] {self.fullname}"

    @property
    def fullname(self) -> str:
        return " ".join([self.surname, self.name, self.patronymic])