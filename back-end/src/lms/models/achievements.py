from django.db import models

from lms.models.students import Student


class AchievementType(models.Model):
    achievement_type = models.CharField(primary_key=True, max_length=100)

    def __str__(self):
        return str(self.achievement_type)

    class Meta:
        verbose_name = 'Achievement Type'
        verbose_name_plural = 'Achievement Types'


class Achievement(models.Model):
    student = models.ForeignKey(Student, models.DO_NOTHING)
    achievement_type = models.ForeignKey(AchievementType, models.DO_NOTHING)
    text = models.TextField()
    date = models.DateField(null=True)

    def __str__(self):
        return f'ID = {str(self.id)}\n' \
               f'StudentID = {str(self.student)}, ' \
               f'Type = {str(self.achievement_type)}\n' \
               f'Date = {str(self.date)}'

    class Meta:
        verbose_name = 'Achievement Journal'
        verbose_name_plural = 'Achievement Journal'
