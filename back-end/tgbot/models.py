from django.db import models


# Create your models here.
class Session(models.Model):
    code = models.CharField(max_length=10)
    chat_id = models.PositiveBigIntegerField(null=True)

    def __str__(self):
        return f'Code:{self.code}, Chat_id:{self.chat_id}'

    class Meta:
        verbose_name = 'Telegram Bot Auth Session'
        verbose_name_plural = 'Telegram Bot Auth Sessions'
