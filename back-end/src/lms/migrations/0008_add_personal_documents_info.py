# Generated by Django 3.2.20 on 2024-02-14 21:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0004_add_personal_documents_info'),
        ('lms', '0007_alter_mark_changed_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='personal_documents_info',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='common.personaldocumentsinfo'),
        ),
    ]
