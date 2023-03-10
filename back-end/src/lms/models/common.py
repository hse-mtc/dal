from django.db import models
from common.models.milspecialties import Milspecialty


class Milfaculty(models.Model):
    title = models.CharField(
        unique=True,
        max_length=127,
    )
    abbreviation = models.CharField(max_length=31)

    class Meta:
        verbose_name = "Military Faculty"
        verbose_name_plural = "Military Faculties"

    def __str__(self):
        return self.title


class Milgroup(models.Model):
    title = models.CharField(
        unique=True,
        max_length=31,
    )
    milfaculty = models.ForeignKey(
        to=Milfaculty,
        on_delete=models.RESTRICT,
    )
    weekday = models.SmallIntegerField()
    archived = models.BooleanField(default=False)
    milspecialty = models.ForeignKey(
        to=Milspecialty,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    class Meta:
        verbose_name = "Military Group"
        verbose_name_plural = "Military Groups"

    def __str__(self):
        return f"[{self.milfaculty}] {self.title}"
