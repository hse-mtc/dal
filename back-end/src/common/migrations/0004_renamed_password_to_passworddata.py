# Generated by Django 3.2.20 on 2023-11-15 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0003_program_available_to_choose_for_applicants'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonalDocuments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('series', models.CharField(max_length=4)),
                ('code', models.CharField(max_length=6)),
                ('ufms_name', models.CharField(max_length=255)),
                ('ufms_code', models.CharField(max_length=7)),
                ('issue_date', models.DateField()),
                ('tax_id', models.CharField(max_length=13)),
                ('insurance_number', models.CharField(max_length=14)),
            ],
            options={
                'verbose_name': 'Passport',
                'verbose_name_plural': 'Passports',
            },
        ),
    ]
