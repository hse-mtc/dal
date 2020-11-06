# Generated by Django 3.1.2 on 2020-11-06 10:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dms', '0011_add_subject_annotation'),
    ]

    operations = [
        migrations.AddField(
            model_name='subject',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL),
        ),
    ]
