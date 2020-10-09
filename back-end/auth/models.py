from django.db import models
from django.contrib.auth import get_user_model


class Profile(models.Model):
    name = models.CharField(max_length=255)
    user = models.OneToOneField(
        to=get_user_model(),
        on_delete=models.CASCADE,
    )
    photo = models.URLField(blank=True)

    def __str__(self):
        return self.name
