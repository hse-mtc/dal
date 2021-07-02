from django.db import models


class Session(models.Model):
    phone = models.CharField(max_length=32)
    chat_id = models.PositiveBigIntegerField(null=True)

    def __str__(self):
        return f'Phone: {self.phone}, chat_id: {self.chat_id}'

    class Meta:
        verbose_name = 'Telegram Bot Auth Session'
        verbose_name_plural = 'Telegram Bot Auth Sessions'
