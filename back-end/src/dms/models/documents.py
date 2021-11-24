import uuid
import datetime

from django.db import models
from django.dispatch import receiver

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


@receiver(models.signals.post_delete)
def auto_delete_file_on_document_delete(sender, instance: Document, **kwargs):
    # pylint: disable=unused-argument
    if not issubclass(sender, Document):
        return

    if instance and instance.file:
        instance.file.delete()


@receiver(models.signals.post_delete, sender=File)
def auto_delete_file_on_file_delete(sender, instance: File, **kwargs):
    # pylint: disable=unused-argument

    if instance and instance.content:
        instance.content.delete(save=False)


@receiver(models.signals.pre_save, sender=File)
def auto_delete_file_on_file_change(sender, instance: File, **kwargs):
    # pylint: disable=unused-argument

    if not instance.pk:
        return

    try:
        old_instance: File = File.objects.get(pk=instance.pk)
    except File.DoesNotExist:
        return
    if old_instance.content != instance.content and old_instance.content:
        old_instance.content.delete(save=False)
