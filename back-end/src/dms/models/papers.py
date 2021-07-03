import datetime

from django.db import models

from taggit.managers import TaggableManager

from dms.models.documents import Document
from dms.models.common import (
    Author,
    Publisher,
)


class Category(models.Model):
    title = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.title


class Paper(Document):
    authors = models.ManyToManyField(to=Author, blank=True)
    category = models.ForeignKey(to=Category, on_delete=models.RESTRICT)
    publication_date = models.DateField(default=datetime.date.today)
    publishers = models.ManyToManyField(to=Publisher, blank=True)
    tags = TaggableManager(blank=True)
    is_binned = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Paper"
        verbose_name_plural = "Papers"
