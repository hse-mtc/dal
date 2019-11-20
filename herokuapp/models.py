from django.db import models
from django.contrib.auth.models import User


class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.URLField(blank=True)
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Documents(models.Model):
    title = models.TextField()
    authors = models.ManyToManyField(UserProfileInfo)

