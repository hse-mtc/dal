# Generated by Django 3.1.8 on 2021-04-25 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0002_auto_20210326_1444'),
    ]

    operations = [
        migrations.AlterField(
            model_name='birthinfo',
            name='city',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='birthinfo',
            name='country',
            field=models.CharField(max_length=64, null=True),
        ),
    ]
