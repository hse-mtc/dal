from django.db import models
from django.contrib.postgres.fields import ArrayField

from lms.models.universities import UniversityInfo


class Milfaculty(models.Model):
    title = models.CharField(
        unique=True,
        max_length=127,
    )
    abbreviation = models.CharField(max_length=31)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Military Faculty"
        verbose_name_plural = "Military Faculties"


class Milgroup(models.Model):
    title = models.CharField(
        unique=True,
        max_length=31,
    )
    milfaculty = models.ForeignKey(
        to=Milfaculty,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    weekday = models.SmallIntegerField()
    archived = models.BooleanField(default=False)

    def __str__(self):
        return f"[{self.milfaculty}] {self.title}"

    class Meta:
        verbose_name = "Military Group"
        verbose_name_plural = "Military Groups"


class Milspecialty(models.Model):
    title = models.CharField(max_length=150)
    code = models.CharField(
        unique=True,
        max_length=31,
    )
    available_for = ArrayField(base_field=models.CharField(
        max_length=2,
        choices=UniversityInfo.Campus.choices,
    ))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Military Specialty"
        verbose_name_plural = "Military Specialties"
