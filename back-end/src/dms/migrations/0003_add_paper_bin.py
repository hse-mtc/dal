# Generated by Django 3.2.3 on 2021-07-03 14:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dms', '0002_make_category_title_unique'),
    ]

    operations = [
        migrations.AddField(
            model_name='paper',
            name='is_binned',
            field=models.BooleanField(default=False),
        ),
    ]