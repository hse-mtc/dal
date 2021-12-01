from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


def super_user_id():
    return 1


class Author(models.Model):
    surname = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
    patronymic = models.CharField(
        max_length=64,
        blank=True,
    )

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"

    def __str__(self) -> str:
        return self.fullname

    @property
    def fullname(self) -> str:
        return " ".join([self.surname, self.name, self.patronymic])


class Publisher(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Publisher"
        verbose_name_plural = "Publishers"

    def __str__(self) -> str:
        return self.name
