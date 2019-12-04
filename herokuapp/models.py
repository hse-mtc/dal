from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager


class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.URLField(blank=True)
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name

# Для отображения имени
class Status(models.Model):
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.status

    class Meta:
        verbose_name = 'Status'
        verbose_name_plural = 'Statuses'


class PublishPlaces(models.Model):
    place = models.CharField(max_length=250)

    def __str__(self):
        return self.place

    class Meta:
        verbose_name = 'Publish place'
        verbose_name_plural = 'Publish places'


class Documents(models.Model):
    title = models.TextField()
    authors = models.ManyToManyField(UserProfileInfo)
    annotation = models.TextField()
    keywords = TaggableManager()
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    published_at = models.DateTimeField()
    published_places = models.ForeignKey(PublishPlaces, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Document'
        verbose_name_plural = 'Documents'


class Subjects(models.Model):
    title = models.CharField(max_length=250)
    abbreviation = models.CharField(max_length=50)

    def __str__(self):
        return self.abbreviation

    class Meta:
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'


class Researches(Documents):
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Research'
        verbose_name_plural = 'Researches'
