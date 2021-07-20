from datetime import date, timedelta
import typing as tp

import uuid
from django.contrib.auth import get_user_model

from django.db import models


class BirthInfo(models.Model):
    date = models.DateField()
    country = models.CharField(max_length=64, null=True)
    city = models.CharField(max_length=64, null=True)

    class Meta:
        verbose_name = "Birth Info"
        verbose_name_plural = "Birth Infos"

    def __str__(self):
        return f"{self.date}, {self.country}, {self.city}"


class ContactInfo(models.Model):
    corporate_email = models.EmailField(null=True, blank=True)
    personal_email = models.EmailField(null=True, blank=True)
    personal_phone_number = models.CharField(
        max_length=32,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Contact Info"
        verbose_name_plural = "Contact Infos"


class Person(models.Model):
    surname = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    patronymic = models.CharField(max_length=32, blank=True)

    citizenship = models.CharField(max_length=64, blank=True)
    permanent_address = models.CharField(max_length=128, blank=True)

    birth_info = models.ForeignKey(
        to=BirthInfo,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    contact_info = models.ForeignKey(
        to=ContactInfo,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    @property
    def full_name(self):
        return " ".join([self.surname, self.name, self.patronymic])

    class Meta:
        abstract = True
        verbose_name = "Person"
        verbose_name_plural = "Persons"

    def __str__(self):
        return self.full_name

    @classmethod
    def get_nearest_birthdays(
        cls,
        filter_kwargs: tp.Optional[dict] = None
    ) -> models.QuerySet[tp.Type["Person"]]:
        """
        Return persons with birthdays that are
        in one week to today's date.
        :return: QuerySet of Person subtype objects
        """
        today = date.today()
        start, end = today, today + timedelta(days=7)
        return cls.objects.select_related("birth_info").filter(
            birth_info__date__day__gte=start.day,
            birth_info__date__day__lte=end.day,
            birth_info__date__month__gte=start.month,
            birth_info__date__month__lte=end.month,
            **({} if filter_kwargs is None else filter_kwargs),
        ).order_by("birth_info__date")


class Relative(Person):

    class Type(models.TextChoices):
        FATHER = "FA", "отец"
        MOTHER = "MO", "мать"
        BROTHER = "BR", "брат"
        SISTER = "SI", "сестра"

    type = models.CharField(max_length=2, choices=Type.choices)

    class Meta:
        verbose_name = "Relative"
        verbose_name_plural = "Relatives"


def upload_to(instance, filename):
    # pylint: disable=unused-argument
    return f"photos/{instance.id}"


class Photo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to=upload_to, blank=True)

    class Meta:
        verbose_name = "PersonPhoto"
        verbose_name_plural = "PersonPhoto"

    def __str__(self) -> str:
        return self.image.name


class Personnel(Person):
    surname_genitive = models.CharField(max_length=32)
    name_genitive = models.CharField(max_length=32)
    patronymic_genitive = models.CharField(max_length=32, blank=True)

    user = models.OneToOneField(
        to=get_user_model(),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    photo = models.OneToOneField(
        to=Photo,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    class Meta:
        abstract = True
        verbose_name = "Personnel"
        verbose_name_plural = "Personnel"
