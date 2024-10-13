from typing import Union

from django.db import models
from django.contrib.postgres.fields import ArrayField

from common.models.universities import Campus, Program
from rest_framework.exceptions import ValidationError
from django.db.models.signals import m2m_changed
from django.dispatch import receiver


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

    selectable_by = models.ManyToManyField(to=Program, blank=True)

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


@receiver(m2m_changed, sender=Milspecialty.selectable_by.through)
def validate_b_titles(
    sender, instance: Milspecialty, action, reverse, model, pk_set, **kwargs
):
    if action in ["post_add", "post_remove", "post_clear"]:
        mismatched_progs = instance.selectable_by.exclude(
            faculty__campus__in=instance.available_for
        )
        if mismatched_progs.exists():
            program: Program = mismatched_progs.first()
            raise ValidationError(
                {
                    "selectable_by": f"Can't make milspecialty {instance} be selectable by program {program}: "
                    f"program's campus ({program.faculty.campus}) is not available for this program"
                }
            )
