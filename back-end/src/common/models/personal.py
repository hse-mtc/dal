import uuid

from django.db import models


class BirthInfo(models.Model):
    date = models.DateField()
    country = models.CharField(
        max_length=64,
        null=True,
    )
    place = models.CharField(
        max_length=64,
        null=True,
    )

    class Meta:
        verbose_name = "Birth Info"
        verbose_name_plural = "Birth Infos"

    def __str__(self) -> str:
        return f"{self.date}, {self.country}, {self.place}"


class ContactInfo(models.Model):
    corporate_email = models.EmailField(
        null=True,
        blank=True,
    )
    personal_email = models.EmailField(
        null=True,
        blank=True,
    )
    personal_phone_number = models.CharField(
        max_length=32,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Contact Info"
        verbose_name_plural = "Contact Infos"


def upload_to(instance, filename):
    # pylint: disable=unused-argument
    return f"photos/{instance.id}"


class Photo(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    image = models.ImageField(
        upload_to=upload_to,
        blank=True,
    )

    class Meta:
        verbose_name = "PersonPhoto"
        verbose_name_plural = "PersonPhoto"

    def __str__(self) -> str:
        return self.image.name


class Passport(models.Model):
    series = models.CharField(max_length=4)
    code = models.CharField(max_length=6)
    ufms_name = models.CharField(max_length=255)
    ufms_code = models.CharField(max_length=7)
    issue_date = models.DateField()

    class Meta:
        verbose_name = "Passport"
        verbose_name_plural = "Passports"


class Relative(models.Model):

    # --------------------------------------------------------------------------
    # Relative-specific enums.

    class Type(models.TextChoices):
        FATHER = "FA", "Отец"
        MOTHER = "MO", "Мать"
        BROTHER = "BR", "Брат"
        SISTER = "SI", "Сестра"

    # --------------------------------------------------------------------------

    surname = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
    patronymic = models.CharField(
        max_length=64,
        blank=True,
    )
    type = models.CharField(
        max_length=2,
        choices=Type.choices,
    )
    citizenship = models.CharField(
        max_length=64,
        blank=True,
    )
    permanent_address = models.CharField(
        max_length=128,
        blank=True,
    )
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

    class Meta:
        verbose_name = "Relative"
        verbose_name_plural = "Relatives"

    def __str__(self) -> str:
        return f"[{self.type.title()}] {self.fullname}"

    @property
    def fullname(self) -> str:
        return " ".join([self.surname, self.name, self.patronymic])
