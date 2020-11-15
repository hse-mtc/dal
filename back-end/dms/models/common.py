from django.db import models
from django.contrib.auth import get_user_model

from common.models import Person

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


class Subject(models.Model):
    title = models.CharField(max_length=255)
    annotation = models.TextField(blank=True)

    # TODO(TmLev): merge migrations, remove default
    user = models.ForeignKey(to=User,
                             on_delete=models.SET_DEFAULT,
                             default=super_user_id)

    class Meta:
        verbose_name = "Subject"
        verbose_name_plural = "Subjects"

    def __str__(self):
        return self.title
