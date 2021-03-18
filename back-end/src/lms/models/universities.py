from django.db import models


class Faculty(models.Model):
    faculty = models.CharField(primary_key=True, max_length=128)

    def __str__(self):
        return str(self.faculty)

    class Meta:
        verbose_name = 'Faculty'
        verbose_name_plural = 'Faculties'


class Program(models.Model):
    code = models.CharField(primary_key=True, max_length=8)
    program = models.CharField(max_length=128, blank=True, null=True)
    faculty = models.ForeignKey(Faculty, models.DO_NOTHING, blank=True)

    def __str__(self):
        return f'({str(self.code)}) {str(self.program)}'

    class Meta:
        verbose_name = 'Educational Program'
        verbose_name_plural = 'Educational Programs'


class UniversityInfo(models.Model):
    program = models.ForeignKey(Program, models.DO_NOTHING)
    group = models.CharField(max_length=32)
    card_id = models.CharField(max_length=32)

    class Meta:
        verbose_name = 'University Info'
        verbose_name_plural = 'University Infos'
