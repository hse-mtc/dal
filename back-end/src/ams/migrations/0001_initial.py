# Generated by Django 3.2.9 on 2021-11-05 16:52

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicationProcess',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mean_grade', models.DecimalField(decimal_places=2, default=0, max_digits=4, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('medical_examination', models.CharField(blank=True, choices=[('FI', 'годен'), ('FMR', 'годен с незначительными ограничениями'), ('FLI', 'ограниченно годен'), ('UR', 'ограниченно не годен'), ('UN', 'не годен')], max_length=3)),
                ('prof_psy_selection', models.CharField(blank=True, choices=[('FI', 'I'), ('SE', 'II'), ('TH', 'III'), ('FO', 'IV')], max_length=2)),
                ('preferential_right', models.BooleanField(default=False)),
                ('characteristic_handed_over', models.BooleanField(default=False)),
                ('criminal_record_handed_over', models.BooleanField(default=False)),
                ('passport_handed_over', models.BooleanField(default=False)),
                ('registration_certificate_handed_over', models.BooleanField(default=False)),
                ('university_card_handed_over', models.BooleanField(default=False)),
                ('application_handed_over', models.BooleanField(default=False)),
                ('pull_ups', models.SmallIntegerField(blank=True, default=None, null=True)),
                ('speed_run', models.FloatField(blank=True, default=None, null=True)),
                ('long_run', models.FloatField(blank=True, default=None, null=True)),
                ('physical_test_grade', models.SmallIntegerField(default=0)),
                ('milspecialty', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='common.milspecialty')),
            ],
            options={
                'verbose_name': 'Application Process',
                'verbose_name_plural': 'Application Processes',
            },
        ),
        migrations.CreateModel(
            name='Applicant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surname', models.CharField(max_length=64)),
                ('name', models.CharField(max_length=64)),
                ('patronymic', models.CharField(blank=True, max_length=64)),
                ('recruitment_office', models.CharField(max_length=255)),
                ('citizenship', models.CharField(blank=True, max_length=64)),
                ('permanent_address', models.CharField(blank=True, max_length=128)),
                ('application_process', models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, to='ams.applicationprocess')),
                ('birth_info', models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, to='common.birthinfo')),
                ('contact_info', models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, to='common.contactinfo')),
                ('family', models.ManyToManyField(blank=True, to='common.Relative')),
                ('passport', models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, to='common.passport')),
                ('photo', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='common.photo')),
                ('university_info', models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, to='common.universityinfo')),
            ],
            options={
                'verbose_name': 'Applicant',
                'verbose_name_plural': 'Applicants',
            },
        ),
    ]
