import datetime
import os

from django.db import models
from django.contrib.auth import get_user_model

from taggit.managers import TaggableManager


def get_upload_path():
    return "documents/"


class Profile(models.Model):
    name = models.CharField(max_length=255)
    user = models.OneToOneField(
        to=get_user_model(),
        on_delete=models.CASCADE,
    )
    photo = models.URLField(blank=True)

    def __str__(self):
        return self.name


class Author(models.Model):
    last_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    patronymic = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Author"
        verbose_name_plural = "Authors"

    def __str__(self):
        return " ".join([self.last_name, self.first_name, self.patronymic])


class Publisher(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Publisher"
        verbose_name_plural = "Publishers"

    def __str__(self):
        return self.name


class Subject(models.Model):
    title = models.CharField(max_length=255)
    abbreviation = models.CharField(max_length=16)

    class Meta:
        verbose_name = "Subject"
        verbose_name_plural = "Subjects"

    def __str__(self):
        return self.title


class Section(models.Model):
    title = models.CharField(max_length=255)
    subject = models.ForeignKey(
        to=Subject,
        on_delete=models.DO_NOTHING,
    )

    class Meta:
        verbose_name = "Section"
        verbose_name_plural = "Sections"

    def __str__(self):
        return self.title


class Topic(models.Model):
    title = models.CharField(max_length=255)
    section = models.ForeignKey(
        to=Section,
        on_delete=models.DO_NOTHING,
    )

    class Meta:
        verbose_name = "Topic"
        verbose_name_plural = "Topics"

    def __str__(self):
        return self.title


class Category(models.Model):
    title = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.title


class File(models.Model):
    content = models.FileField(
        upload_to=get_upload_path(),
        blank=True,
    )

    def get_file_extension(self):
        _, extension = os.path.splitext(self.content.name)
        return extension

    def get_file_name(self):
        return self.content.name


class Document(models.Model):
    title = models.TextField()
    authors = models.ManyToManyField(
        to=Author,
        blank=True,
    )
    annotation = models.TextField(blank=True)
    tags = TaggableManager(blank=True)
    category = models.ForeignKey(
        to=Category,
        on_delete=models.CASCADE,
    )
    publication_date = models.DateField(default=datetime.date.today)
    publishers = models.ManyToManyField(
        to=Publisher,
        blank=True,
    )
    topic = models.ForeignKey(
        to=Topic,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )
    subject = models.ForeignKey(
        to=Subject,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
    )
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    is_in_trash = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Document"
        verbose_name_plural = "Documents"

    def __str__(self):
        return self.title
