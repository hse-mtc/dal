# Generated by Django 3.1.7 on 2021-04-02 15:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lesson',
            old_name='lesson_type',
            new_name='type',
        ),
    ]
