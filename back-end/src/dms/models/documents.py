import uuid
import datetime

from django.db import models

from dms.models.common import (
    User,
    super_user_id,
)


def upload_to(instance, filename):
    # pylint: disable=unused-argument
    return f"files/{instance.id}"


class File(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.FileField(upload_to=upload_to, blank=True)
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = "File"
        verbose_name_plural = "Files"

    def __str__(self):
        return self.name

    def get_extension(self):
        return self.name.rsplit(".", maxsplit=1)[-1]


class Document(models.Model):
    """Document represents abstract document of any type.

    It holds fields necessary for all inherited document models.
    """

    title = models.TextField(blank=True)
    annotation = models.TextField(blank=True)
    file = models.ForeignKey(to=File, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User,
                             on_delete=models.SET_DEFAULT,
                             default=super_user_id)
    upload_date = models.DateField(default=datetime.date.today)

    class Meta:
        abstract = True
        verbose_name = "Document"
        verbose_name_plural = "Documents"

    def __str__(self):
        return self.title
