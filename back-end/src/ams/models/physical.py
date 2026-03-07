from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver

from ams.models.applicants import ApplicationProcess
from ams.physical.exercises import ExerciseType


class ExerciseResult(models.Model):
    application_process = models.ForeignKey(
        to=ApplicationProcess,
        on_delete=models.CASCADE,
        related_name="exercise_results",
    )
    exercise_type = models.CharField(
        max_length=32,
        choices=ExerciseType.choices,
    )
    value = models.FloatField()
    extra_params = models.JSONField(
        default=dict,
        blank=True,
    )
    secondary_score = models.SmallIntegerField(default=0)

    class Meta:
        verbose_name = "Exercise Result"
        verbose_name_plural = "Exercise Results"
        unique_together = ("application_process", "exercise_type")

    def __str__(self) -> str:
        return (
            f"[{self.id}] {self.get_exercise_type_display()}: "
            f"{self.value} → {self.secondary_score}"
        )

    def save(self, *args, **kwargs):
        """Автоматический пересчет баллов при сохранении."""
        # Избегаем рекурсии: если обновляется только secondary_score, не пересчитываем
        update_fields = kwargs.get("update_fields")
        should_recalculate = (
            update_fields is None
            or "secondary_score" not in update_fields
            or len(update_fields) > 1
        )

        super().save(*args, **kwargs)

        if should_recalculate:
            # Избегаем циклического импорта
            from ams.physical.recalculate import recalculate_physical_scores

            recalculate_physical_scores(self.application_process)


@receiver(post_delete, sender=ExerciseResult)
def recalculate_on_delete(sender, instance, **kwargs):
    """Пересчет баллов при удалении результата."""
    from ams.physical.recalculate import recalculate_physical_scores

    recalculate_physical_scores(instance.application_process)
