# Generated by Django 3.2.20 on 2023-11-15 07:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0004_renamed_password_to_passworddata'),
        ('lms', '0007_alter_mark_changed_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='passport',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='common.personaldocuments'),
        ),
    ]