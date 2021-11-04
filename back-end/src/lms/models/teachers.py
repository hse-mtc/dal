from django.db import models
from django.contrib.auth import get_user_model

from common.models.personal import (
    BirthInfo,
    ContactInfo,
    Name,
    Photo,
)

from lms.models.common import (
    Milfaculty,
    Milgroup,
)


class Teacher(models.Model):

    # --------------------------------------------------------------------------

    class Post(models.TextChoices):
        MTC_HEAD = "CH", "начальник ВУЦ"
        MILFACULTY_HEAD = "FH", "начальник цикла"
        TEACHERS = "TE", "профессорско-преподавательский состав"

    class Rank(models.TextChoices):
        CAPTAIN = "CA", "капитан"
        MAJOR = "MA", "майор"
        LIEUTENANT_COLONEL = "LC", "подполковник"
        COLONEL = "CO", "полковник"
        MAJOR_GENERAL = "MG", "генерал-майор"

    # --------------------------------------------------------------------------
    # Frequently accessed data.

    name = models.ForeignKey(
        to=Name,
        on_delete=models.RESTRICT,
    )
    user = models.ForeignKey(
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

    photo = models.ForeignKey(
        to=Photo,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    birth_info = models.ForeignKey(
        to=BirthInfo,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    contact_info = models.ForeignKey(
        to=ContactInfo,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Teacher"
        verbose_name_plural = "Teachers"

    def __str__(self):
        return f"[{self.id}] {self.name}"
