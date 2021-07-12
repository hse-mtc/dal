from django.db import models

from common.models.persons import Personnel

from lms.models.common import (
    Milfaculty,
    Milgroup,
)


class Rank(models.Model):
    title = models.CharField(
        unique=True,
        max_length=63,
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Military Rank"
        verbose_name_plural = "Military Ranks"


class Teacher(Personnel):

    class Post(models.TextChoices):
        MTC_HEAD = "CH", "начальник ВУЦ"
        MILFACULTY_HEAD = "FH", "начальник цикла"
        TEACHERS = "TE", "профессорско-преподавательский состав"

    post = models.CharField(
        max_length=2,
        choices=Post.choices,
        default=Post.TEACHERS.value,
        null=True,
        blank=True,
    )
    rank = models.ForeignKey(
        to=Rank,
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

    def __str__(self):
        return f"ID = {str(self.id)}\n" \
               f"Full name = {str(self.surname)} " \
               f"{str(self.name)} {str(self.patronymic)}\n"

    class Meta:
        verbose_name = "Teacher"
        verbose_name_plural = "Teachers"
