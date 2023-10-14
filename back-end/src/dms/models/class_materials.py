from django.db import models
from django.db.models import Max
from django.dispatch import receiver

from ordered_model.models import OrderedModel

from dms.models.documents import Document
from common.models.subjects import Subject


class Section(OrderedModel):
    title = models.CharField(max_length=255)
    subject = models.ForeignKey(
        to=Subject, on_delete=models.CASCADE, related_name="sections"
    )
    order_with_respect_to = "subject"

    class Meta(OrderedModel.Meta):
        verbose_name = "Section"
        verbose_name_plural = "Sections"

    def __str__(self):
        return self.title


class Topic(OrderedModel):
    title = models.CharField(max_length=255)
    annotation = models.TextField(blank=True)
    section = models.ForeignKey(
        to=Section, on_delete=models.CASCADE, related_name="topics"
    )
    order_with_respect_to = "section__subject"

    def save(self, *args, **kwargs):
        is_new = not self.id
        order = (
            Topic.objects.filter(
                section__subject=self.section.subject,
                section__order__lte=self.section.order,
            )
            .aggregate(Max("order"))
            .get("order__max")
        )
        super().save(*args, **kwargs)

        if is_new:
            if order is not None:
                order = order + 1
            else:
                order = 0

            self.to(order)

    class Meta(OrderedModel.Meta):
        verbose_name = "Topic"
        verbose_name_plural = "Topics"

    def __str__(self):
        return self.title


def update_topics_in_subject_of_section(instance: Section):
    tops = Topic.objects.filter(section__subject=instance.subject)
    updated_instances = []

    for index, instance in enumerate(tops.order_by("section__order", "order")):
        instance.order = index
        updated_instances.append(instance)
    Topic.objects.bulk_update(updated_instances, ["order"])


@receiver(models.signals.post_save, sender=Section)
def update_section_order(sender: Section, instance: Section, **kwargs):
    # pylint: disable=unused-argument
    if not isinstance(instance, Section):
        return
    update_topics_in_subject_of_section(instance)


@receiver(models.signals.post_delete, sender=Section)
def update_section_order(sender: Section, instance: Section, **kwargs):
    # pylint: disable=unused-argument
    if not isinstance(instance, Section):
        return
    update_topics_in_subject_of_section(instance)


class ClassMaterial(Document):
    # TODO(TmLev): Extract to `common` so that `lms.Lesson` can use this too.
    class Type(models.TextChoices):
        LECTURES = "LE", "lectures"
        SEMINARS = "SE", "seminars"
        GROUPS = "GR", "groups"
        PRACTICES = "PR", "practices"

    type = models.CharField(max_length=2, choices=Type.choices)
    topic = models.ForeignKey(
        to=Topic, on_delete=models.CASCADE, related_name="class_materials"
    )

    class Meta:
        verbose_name = "Class Material"
        verbose_name_plural = "Class Materials"
