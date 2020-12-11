from django.db import models


class Person(models.Model):
    surname = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    patronymic = models.CharField(max_length=32, blank=True)

    @property
    def full_name(self):
        return " ".join([self.surname, self.name, self.patronymic])

    class Meta:
        abstract = True
        verbose_name = "Person"
        verbose_name_plural = "Persons"

    def __str__(self):
        return self.full_name
