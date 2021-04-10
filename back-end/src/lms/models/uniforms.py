from django.db import models

from lms.models.common import Milfaculty


class Uniform(models.Model):

    class Headdress(models.TextChoices):
        CAP = 'CA', 'Кепка'
        HAT = 'HA', 'Шапка'

    class Outerwear(models.TextChoices):
        PEA_COAT = 'PC', 'Бушлат'
        JACKET = 'JA', 'Китель'

    headdress = models.CharField(max_length=2, choices=Headdress.choices)
    outerwear = models.CharField(max_length=2, choices=Outerwear.choices)
    milfaculty = models.ForeignKey(Milfaculty, models.DO_NOTHING)

    def __str__(self):
        return f'{str(self.headdress)} + {str(self.outerwear)}'

    class Meta:
        verbose_name = 'Current uniform'
        verbose_name_plural = 'Current uniforms'
