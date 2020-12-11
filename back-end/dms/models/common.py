from django.db import models
from django.contrib.auth import get_user_model

from common.models.persons import Person

User = get_user_model()


def super_user_id():
    return 1


class Author(Person):

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"


class Publisher(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Publisher"
        verbose_name_plural = "Publishers"

    def __str__(self):
        return self.name
