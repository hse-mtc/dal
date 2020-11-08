from django.db import models
from django.contrib.auth import get_user_model

from common.models import Person


class Profile(Person):
    user = models.OneToOneField(to=get_user_model(), on_delete=models.CASCADE)
    photo = models.URLField(blank=True)

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"
