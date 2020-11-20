# Generated by Django 3.1.3 on 2020-11-20 11:21

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AbsenceStatus',
            fields=[
                ('absence_status', models.CharField(max_length=100, primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name': 'Absence Status',
                'verbose_name_plural': 'Absence Statuses',
            },
        ),
        migrations.CreateModel(
            name='AbsenceType',
            fields=[
                ('absence_type', models.CharField(max_length=100, primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name': 'Absence Type',
                'verbose_name_plural': 'Absence Types',
            },
        ),
        migrations.CreateModel(
            name='EncouragementType',
            fields=[
                ('encouragement_type', models.CharField(max_length=100, primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name': 'Encouragement Type',
                'verbose_name_plural': 'Encouragement Types',
            },
        ),
        migrations.CreateModel(
            name='Milfaculty',
            fields=[
                ('milfaculty', models.CharField(max_length=10, primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name': 'Military Faculty',
                'verbose_name_plural': 'Military Faculties',
            },
        ),
        migrations.CreateModel(
            name='Milgroup',
            fields=[
                ('milgroup', models.DecimalField(decimal_places=0, max_digits=4, primary_key=True, serialize=False)),
                ('weekday', models.DecimalField(decimal_places=0, max_digits=1)),
                ('milfaculty', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='lms.milfaculty')),
            ],
            options={
                'verbose_name': 'Military Group',
                'verbose_name_plural': 'Military Groups',
            },
        ),
        migrations.CreateModel(
            name='Program',
            fields=[
                ('code', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('program', models.CharField(blank=True, max_length=500, null=True)),
            ],
            options={
                'verbose_name': 'Educational Program',
                'verbose_name_plural': 'Educational Programs',
            },
        ),
        migrations.CreateModel(
            name='PunishmentType',
            fields=[
                ('punishment_type', models.CharField(max_length=100, primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name': 'Punishment Type',
                'verbose_name_plural': 'Punishment Types',
            },
        ),
        migrations.CreateModel(
            name='Rank',
            fields=[
                ('rank', models.CharField(max_length=30, primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name': 'Military Rank',
                'verbose_name_plural': 'Military Ranks',
            },
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('status', models.CharField(max_length=20, primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name': 'Student Status',
                'verbose_name_plural': 'Student Statuses',
            },
        ),
        migrations.CreateModel(
            name='TeacherPost',
            fields=[
                ('teacher_post', models.CharField(max_length=100, primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name': 'Teacher Post',
                'verbose_name_plural': 'Teacher Posts',
            },
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surname', models.CharField(max_length=32)),
                ('name', models.CharField(max_length=32)),
                ('patronymic', models.CharField(blank=True, max_length=32)),
                ('milfaculty', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='lms.milfaculty')),
                ('milgroup', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='lms.milgroup')),
                ('rank', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='lms.rank')),
                ('teacher_post', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='lms.teacherpost')),
            ],
            options={
                'verbose_name': 'Teacher',
                'verbose_name_plural': 'Teachers',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surname', models.CharField(max_length=32)),
                ('name', models.CharField(max_length=32)),
                ('patronymic', models.CharField(blank=True, max_length=32)),
                ('birthdate', models.DateField()),
                ('photo', models.CharField(blank=True, max_length=128, null=True)),
                ('milgroup', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='lms.milgroup')),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='lms.program')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='lms.status')),
            ],
            options={
                'verbose_name': 'Student',
                'verbose_name_plural': 'Students',
            },
        ),
        migrations.CreateModel(
            name='Punishment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(max_length=200)),
                ('date', models.DateField(default=datetime.date.today)),
                ('remove_date', models.DateField(blank=True, null=True)),
                ('punishment_type', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='lms.punishmenttype')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='lms.student')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='lms.teacher')),
            ],
            options={
                'verbose_name': 'Punishment Journal',
                'verbose_name_plural': 'Punishment Journal',
            },
        ),
        migrations.CreateModel(
            name='Encouragement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(max_length=200)),
                ('date', models.DateField(default=datetime.date.today)),
                ('encouragement_type', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='lms.encouragementtype')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='lms.student')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='lms.teacher')),
            ],
            options={
                'verbose_name': 'Encouragement Journal',
                'verbose_name_plural': 'Encouragement Journal',
            },
        ),
        migrations.CreateModel(
            name='Absence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date.today)),
                ('reason', models.CharField(blank=True, max_length=100, null=True)),
                ('comment', models.CharField(blank=True, max_length=100, null=True)),
                ('absence_status', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='lms.absencestatus')),
                ('absence_type', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='lms.absencetype')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lms.student')),
            ],
            options={
                'verbose_name': 'Absence Journal',
                'verbose_name_plural': 'Absence Journal',
                'unique_together': {('date', 'student')},
            },
        ),
    ]
