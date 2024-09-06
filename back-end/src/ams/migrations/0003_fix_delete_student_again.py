# Generated by Django 3.2.20 on 2024-09-06 09:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('common', '0003_program_available_to_choose_for_applicants'),
        ('ams', '0002_applicationprocess_mtc_admission_year'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicant',
            name='contact_info',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='common.contactinfo'),
        ),
        migrations.AlterField(
            model_name='applicant',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
