from django.db import models


class Faculty(models.Model):
    title = models.CharField(
        unique=True,
        max_length=127,
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Faculty"
        verbose_name_plural = "Faculties"


class Program(models.Model):
    code = models.CharField(
        unique=True,
        max_length=8,
    )
    title = models.CharField(
        max_length=127,
        blank=True,
        null=True,
    )
    faculty = models.ForeignKey(
        to=Faculty,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"({self.code}) {self.title}"

    class Meta:
        verbose_name = "Educational Program"
        verbose_name_plural = "Educational Programs"


class UniversityInfo(models.Model):

    class Campus(models.TextChoices):
        MOSCOW = "MO", "Москва"
        SAINT_PETERSBURG = "SP", "Санкт-Петербург"
        NIZHNY_NOVGOROD = "NN", "Нижний Новгород"
        PERM = "PE", "Пермь"

    campus = models.CharField(
        max_length=2,
        choices=Campus.choices,
    )
    program = models.ForeignKey(
        to=Program,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    group = models.CharField(max_length=32)
    card_id = models.CharField(max_length=32)

    class Meta:
        verbose_name = "University Info"
        verbose_name_plural = "University Infos"
