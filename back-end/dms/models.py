import datetime
import uuid

from django.db import models
from django.contrib.auth import get_user_model

from taggit.managers import TaggableManager


def upload_to(instance, filename):
    # pylint: disable=unused-argument
    return f"files/{instance.id}/"


def current_year():
    return datetime.date.today().year


def super_user_id():
    return 1


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
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.FileField(upload_to=upload_to, blank=True)
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "File"
        verbose_name_plural = "Files"

    def __str__(self):
        return self.name

    def get_extension(self):
        return self.name.split(".")[-1]


class Document(models.Model):
    """Document represents abstract document of any type.

    It holds fields necessary for all inherited document models.
    """

    title = models.TextField()
    annotation = models.TextField(blank=True)
    file = models.ForeignKey(to=File, on_delete=models.CASCADE)
    user = models.ForeignKey(to=get_user_model(),
                             on_delete=models.SET_DEFAULT,
                             default=super_user_id())

    class Meta:
        abstract = True
        verbose_name = "Document"
        verbose_name_plural = "Documents"

    def __str__(self):
        return self.title


class Paper(Document):
    authors = models.ManyToManyField(to=Author, blank=True)
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE)
    publication_date = models.DateField(default=datetime.date.today)
    publishers = models.ManyToManyField(to=Publisher, blank=True)
    tags = TaggableManager(blank=True)

    class Meta:
        verbose_name = "Paper"
        verbose_name_plural = "Papers"


class ClassMaterial(Document):

    class Type(models.TextChoices):
        LECTURES = "LE", "lectures"
        SEMINARS = "SE", "seminars"
        GROUPS = "GR", "groups"
        PRACTICES = "PR", "practices"

    type = models.CharField(max_length=2, choices=Type.choices)
    topic = models.ForeignKey(to=Topic, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Class Material"
        verbose_name_plural = "Class Materials"


class Book(Document):
    authors = models.ManyToManyField(to=Author, blank=True)
    publication_year = models.PositiveSmallIntegerField(default=current_year)
    publishers = models.ManyToManyField(to=Publisher, blank=True)
    subjects = models.ManyToManyField(to=Subject, blank=True)

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"
