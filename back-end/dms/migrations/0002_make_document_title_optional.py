# Generated by Django 3.1.3 on 2020-11-20 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dms', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='title',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='classmaterial',
            name='title',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='paper',
            name='title',
            field=models.TextField(blank=True),
        ),
    ]
