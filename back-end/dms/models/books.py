import datetime

from django.db import models

from dms.models.documents import Document
from dms.models.common import (
    Author,
    Publisher,
    Subject,
)


def current_year():
    return datetime.date.today().year


class Book(Document):
    authors = models.ManyToManyField(to=Author, blank=True)
    publication_year = models.PositiveSmallIntegerField(default=current_year)
    publishers = models.ManyToManyField(to=Publisher, blank=True)
    subjects = models.ManyToManyField(to=Subject, blank=True)

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"
