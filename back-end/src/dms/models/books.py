import datetime
import uuid

from django.db import models

from dms.models.documents import Document
from dms.models.common import (
    Author,
    Publisher,
    User,
)

from common.models.subjects import Subject


def upload_to(instance, filename):
    # pylint: disable=unused-argument
    return f"covers/{instance.id}"


class Cover(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to=upload_to, blank=True)

    class Meta:
        verbose_name = "Cover"
        verbose_name_plural = "Covers"

    def __str__(self) -> str:
        return self.image.name


def current_year():
    return datetime.date.today().year


class Book(Document):
    authors = models.ManyToManyField(to=Author, blank=True)
    publication_year = models.PositiveSmallIntegerField(default=current_year)
    publishers = models.ManyToManyField(to=Publisher, blank=True)
    subjects = models.ManyToManyField(to=Subject, blank=True)
    cover = models.OneToOneField(to=Cover, on_delete=models.CASCADE, null=True)
    page_count = models.PositiveSmallIntegerField(null=True, default=None)

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"


class FavoriteBook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Favorite book"
        verbose_name_plural = "Favorite books"

    def __str__(self):
        return f"{self.user} - {self.book}"
