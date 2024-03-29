import uuid

from django.db import models

from django.dispatch import receiver


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
        unique=True,
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


@receiver(models.signals.post_delete, sender=Photo)
def auto_delete_image_on_cover_delete(sender, instance: Photo, **kwargs):
    # pylint: disable=unused-argument

    if instance and instance.image:
        instance.image.delete(save=False)


class Passport(models.Model):
    series = models.CharField(max_length=4)
    code = models.CharField(max_length=6)
    ufms_name = models.CharField(max_length=255)
    ufms_code = models.CharField(max_length=7)
    issue_date = models.DateField()

    class Meta:
        verbose_name = "Passport"
        verbose_name_plural = "Passports"


class PersonalDocumentsInfo(models.Model):
    tax_id = models.CharField(max_length=13, null=False)
    insurance_number = models.CharField(max_length=14, null=False)

    class Meta:
        verbose_name = "Personal Documents Info"
        verbose_name_plural = "Personal Documents Infos"


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
