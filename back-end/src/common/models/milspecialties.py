from typing import Union

from django.db import models
from django.contrib.postgres.fields import ArrayField

from common.models.universities import Campus, Program
from django.core.exceptions import ValidationError


class Milspecialty(models.Model):
    title = models.CharField(max_length=150)
    code = models.CharField(
        unique=True,
        max_length=31,
    )
    available_for = ArrayField(
        base_field=models.CharField(
            max_length=2,
            choices=Campus.choices,
        )
    )

    selectable_by = models.ManyToManyField(
        to=Program
    )

    selectable_by_every_program = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Military Specialty"
        verbose_name_plural = "Military Specialties"

    def __str__(self) -> str:
        return self.title

    def check_campuses_match(self):
        if self.pk:
            for program in self.selectable_by.all():
                if program.faculty.campus not in self.available_for:
                    raise ValidationError(
                        f"Can't make milspecialty {self.milspecialty} be selectable by program {self.program}: "
                        f"program's campus ({self.program.faculty.campus}) is not available for this program"
                    )

    def save(self, *args, **kwargs):
        self.check_campuses_match()
        super().save(*args, **kwargs)

    def is_selectable_by_program(self, program_: Union[Program, int]):
        if isinstance(program_, Program):
            program = program_.pk
        else:
            program = program_
        return (
            self.selectable_by.filter(pk=program).exists()
            or self.selectable_by_every_program
        )
