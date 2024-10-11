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
        to=Program, through="MilspecialtySelectableByProgram"
    )

    selectable_by_every_program = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Military Specialty"
        verbose_name_plural = "Military Specialties"

    def __str__(self) -> str:
        return self.title

    def is_selectable_by_program(self, program_: Union[Program, int]):
        if isinstance(program_, Program):
            program = program_.pk
        else:
            program = program_
        return (
                self.selectable_by.filter(pk=program).exists()
                or self.selectable_by_every_program
            )


class MilspecialtySelectableByProgram(models.Model):
    milspecialty = models.ForeignKey(Milspecialty, on_delete=models.CASCADE)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Milspecialty selectable by program"
        verbose_name_plural = "Milspecialties selectable by programs"
        constraints = [
            models.UniqueConstraint(
                fields=["milspecialty", "program"],
                name="unique_milspecialty_selectable_by_program_relation",
            )
        ]

    def check_campus_match(self):
        if self.program.faculty.campus not in self.milspecialty.available_for:
            raise ValidationError(
                f"Can't make milspecialty {self.milspecialty} be selectable by program {self.program}: "
                f"program's campus ({self.program.faculty.campus}) is not available for this program"
            )

    def save(self, *args, **kwargs):
        self.check_campus_match()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.milspecialty.title} selectable by {self.program.title}"
