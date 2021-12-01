from django.db import models
from django.contrib.postgres.fields import ArrayField


from common.models.universities import Campus


class Milspecialty(models.Model):
    title = models.CharField(max_length=150)
    code = models.CharField(
        unique=True,
        max_length=31,
    )
    available_for = ArrayField(base_field=models.CharField(
        max_length=2,
        choices=Campus.choices,
    ))

    class Meta:
        verbose_name = "Military Specialty"
        verbose_name_plural = "Military Specialties"

    def __str__(self) -> str:
        return self.title
