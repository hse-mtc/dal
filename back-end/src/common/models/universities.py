from django.db import models


class Campus(models.TextChoices):
    MOSCOW = "MO", "Москва"
    SAINT_PETERSBURG = "SP", "Санкт-Петербург"
    NIZHNY_NOVGOROD = "NN", "Нижний Новгород"
    PERM = "PE", "Пермь"


class Faculty(models.Model):
    campus = models.CharField(
        choices=Campus.choices,
        max_length=2,
    )
    title = models.CharField(max_length=255)
    abbreviation = models.CharField(
        max_length=31,
        blank=True,
    )

    def __str__(self):
        return f"[{self.campus}] {self.title}"

    class Meta:
        verbose_name = "Faculty"
        verbose_name_plural = "Faculties"
        unique_together = [["campus", "title"]]


class Program(models.Model):
    code = models.CharField(max_length=63)
    title = models.CharField(max_length=127)
    faculty = models.ForeignKey(
        to=Faculty,
        on_delete=models.RESTRICT,
    )
    available_to_choose_for_applicants = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.faculty.campus} [{self.code}] {self.title}"

    @property
    def digit_code(self) -> str:
        words = self.code.split()
        if len(words) > 0:
            return words[0]
        return ""

    class Meta:
        verbose_name = "Educational Program"
        verbose_name_plural = "Educational Programs"


class UniversityInfo(models.Model):
    program = models.ForeignKey(
        to=Program,
        on_delete=models.RESTRICT,
    )
    group = models.CharField(max_length=32)
    card_id = models.CharField(max_length=32)
    graduation_year = models.IntegerField(
        default=None,
        null=True,
        blank=False,
        verbose_name="Год окончания вуза",
    )

    class Meta:
        verbose_name = "University Info"
        verbose_name_plural = "University Infos"

    @property
    def campus(self) -> str:
        return self.program.faculty.campus
