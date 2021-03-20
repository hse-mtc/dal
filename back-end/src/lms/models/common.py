from django.db import models
from django.contrib.postgres.fields import ArrayField

from lms.models.universities import UniversityInfo


class Milfaculty(models.Model):
    milfaculty = models.CharField(primary_key=True, max_length=10)

    def __str__(self):
        return str(self.milfaculty)

    class Meta:
        verbose_name = 'Military Faculty'
        verbose_name_plural = 'Military Faculties'


class Milspecialty(models.Model):
    code = models.CharField(primary_key=True, max_length=20)
    milspecialty = models.CharField(max_length=150)
    available_for = ArrayField(
        base_field=models.CharField(
            max_length=2,
            choices=UniversityInfo.Campus.choices,
        ),
    )

    def __str__(self):
        return str(self.milspecialty)

    class Meta:
        verbose_name = 'Military specialty'
        verbose_name_plural = 'Military specialties'


class Milgroup(models.Model):
    milgroup = models.DecimalField(primary_key=True,
                                   max_digits=4,
                                   decimal_places=0)
    milfaculty = models.ForeignKey(Milfaculty, models.DO_NOTHING)
    weekday = models.DecimalField(max_digits=1, decimal_places=0)

    def __str__(self):
        return f'{str(self.milgroup)}, {str(self.milfaculty)}'

    class Meta:
        verbose_name = 'Military Group'
        verbose_name_plural = 'Military Groups'
