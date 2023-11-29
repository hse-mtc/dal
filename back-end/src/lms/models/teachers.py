from django.db import models
from django.contrib.auth import get_user_model

from django.dispatch import receiver

from common.models.personal import (
    BirthInfo,
    ContactInfo,
    Photo,
)

from lms.models.common import (
    Milfaculty,
    Milgroup,
)


class Teacher(models.Model):
    # --------------------------------------------------------------------------

    class Post(models.TextChoices):
        MTC_HEAD = "CH", "Начальник ВУЦ"
        MILFACULTY_HEAD = "FH", "Начальник цикла"
        TEACHERS = "TE", "Профессорско-преподавательский состав"

    class Rank(models.TextChoices):
        LIEUTENANT = "LI", "Лейтенант"
        SENIOR_LIEUTENANT = "SL", "Старший лейтенант"
        CAPTAIN = "CA", "Капитан"
        MAJOR = "MA", "Майор"
        LIEUTENANT_COLONEL = "LC", "Подполковник"
        COLONEL = "CO", "Полковник"
        MAJOR_GENERAL = "MG", "Генерал-майор"

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
    milfaculty = models.ForeignKey(
        to=Milfaculty,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    milgroups = models.ManyToManyField(
        to=Milgroup,
        blank=True,
    )

    # --------------------------------------------------------------------------
    # Rarely accessed studying data.

    post = models.CharField(
        max_length=2,
        choices=Post.choices,
        default=Post.TEACHERS.value,
    )
    rank = models.CharField(
        max_length=2,
        choices=Rank.choices,
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

    class Meta:
        verbose_name = "Teacher"
        verbose_name_plural = "Teachers"

    def __str__(self):
        return f"[{self.id}] {self.fullname}"

    @property
    def fullname(self) -> str:
        return " ".join([self.surname, self.name, self.patronymic])


@receiver(models.signals.post_delete, sender=Teacher)
def post_delete_fields(sender, instance: Teacher, **kwargs):
    attributes_to_delete = [
        "user",
        "contact_info",
        "birth_info",
        "photo",
    ]
    for attr in attributes_to_delete:
        attr_to_delete = getattr(instance, attr, None)
        if attr_to_delete is not None:
            attr_to_delete.delete()
