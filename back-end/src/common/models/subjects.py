from django.db import models
from django.contrib.auth import get_user_model

from common.models.milspecialties import Milspecialty

User = get_user_model()


def super_user_id():
    return 1


class Subject(models.Model):
    title = models.CharField(max_length=255)
    annotation = models.TextField(blank=True)
    milspecialty = models.ForeignKey(to=Milspecialty, on_delete=models.CASCADE, default=None, null=True, related_name="milspecialties")

    # TODO(TmLev): merge migrations, remove default
    user = models.ForeignKey(
        to=User, on_delete=models.SET_DEFAULT, default=super_user_id
    )

    class Meta:
        verbose_name = "Subject"
        verbose_name_plural = "Subjects"

    def __str__(self):
        return self.title
