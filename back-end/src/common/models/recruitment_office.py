from django.db import models


class RecruitmentOffice(models.Model):
    city = models.CharField(max_length=64)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Recruitment Office"
        verbose_name_plural = "Recruitment Offices"
