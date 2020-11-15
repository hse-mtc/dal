from django.db import models

from ordered_model.models import OrderedModel

from dms.models.common import Subject
from dms.models.documents import Document


class Section(OrderedModel):
    title = models.CharField(max_length=255)
    subject = models.ForeignKey(to=Subject, on_delete=models.CASCADE)
    order_with_respect_to = "subject"

    class Meta(OrderedModel.Meta):
        verbose_name = "Section"
        verbose_name_plural = "Sections"

    def __str__(self):
        return self.title


class Topic(OrderedModel):
    title = models.CharField(max_length=255)
    annotation = models.TextField(blank=True)
    section = models.ForeignKey(to=Section, on_delete=models.CASCADE)
    order_with_respect_to = "section"

    class Meta(OrderedModel.Meta):
        verbose_name = "Topic"
        verbose_name_plural = "Topics"

    def __str__(self):
        return self.title


class ClassMaterial(Document):

    class Type(models.TextChoices):
        LECTURES = "LE", "lectures"
        SEMINARS = "SE", "seminars"
        GROUPS = "GR", "groups"
        PRACTICES = "PR", "practices"

    type = models.CharField(max_length=2, choices=Type.choices)
    topic = models.ForeignKey(to=Topic, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Class Material"
        verbose_name_plural = "Class Materials"
