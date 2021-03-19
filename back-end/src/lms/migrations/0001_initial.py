# Generated by Django 3.1.7 on 2021-03-19 10:11

import datetime
import django.contrib.postgres.fields
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
            name='AbsenceTime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('absence_restriction_time', models.TimeField()),
            ],
            options={
                'verbose_name': 'Absence Time',
                'verbose_name_plural': 'Abcense Time',
            },
        ),
        migrations.CreateModel(
            name='AchievementType',
            fields=[
                ('achievement_type', models.CharField(max_length=100, primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name': 'Achievement Type',
                'verbose_name_plural': 'Achievement Types',
            },
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('faculty', models.CharField(max_length=128, primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name': 'Faculty',
                'verbose_name_plural': 'Faculties',
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lesson_type', models.CharField(choices=[('LE', 'Лекция'), ('SE', 'Семинар'), ('GR', 'Групповое занятие'), ('PR', 'Практическое занятие'), ('FI', 'Зачет'), ('EX', 'Экзамен')], max_length=2)),
                ('date', models.DateField(default=datetime.date.today)),
                ('ordinal', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(1)])),
            ],
            options={
                'verbose_name': 'Lesson',
                'verbose_name_plural': 'Lessons',
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
            name='Milspecialty',
            fields=[
                ('code', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('milspecialty', models.CharField(max_length=150)),
            ],
            options={
                'verbose_name': 'Military specialty',
                'verbose_name_plural': 'Military specialties',
            },
        ),
        migrations.CreateModel(
            name='Passport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('series', models.CharField(max_length=4)),
                ('code', models.CharField(max_length=6)),
                ('ufms_name', models.CharField(max_length=255)),
                ('ufms_code', models.CharField(max_length=7)),
                ('issue_date', models.DateField()),
            ],
            options={
                'verbose_name': 'Passport',
                'verbose_name_plural': 'Passports',
            },
        ),
        migrations.CreateModel(
            name='Program',
            fields=[
                ('code', models.CharField(max_length=8, primary_key=True, serialize=False)),
                ('program', models.CharField(blank=True, max_length=128, null=True)),
                ('faculty', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.DO_NOTHING, to='lms.faculty')),
            ],
            options={
                'verbose_name': 'Educational Program',
                'verbose_name_plural': 'Educational Programs',
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
            name='RecruitmentOffice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(max_length=32)),
                ('district', models.CharField(max_length=32)),
            ],
            options={
                'verbose_name': 'Recruitment Office',
                'verbose_name_plural': 'Recruitment Offices',
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('room', models.CharField(max_length=50, primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name': 'Room',
                'verbose_name_plural': 'Rooms',
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
            name='UniversityInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.CharField(max_length=32)),
                ('card_id', models.CharField(max_length=32)),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='lms.program')),
            ],
            options={
                'verbose_name': 'University Info',
                'verbose_name_plural': 'University Infos',
            },
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surname', models.CharField(max_length=32)),
                ('name', models.CharField(max_length=32)),
                ('patronymic', models.CharField(blank=True, max_length=32)),
                ('citizenship', models.CharField(max_length=64, null=True)),
                ('permanent_address', models.CharField(max_length=128, null=True)),
                ('birth_info', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='common.birthinfo')),
                ('contact_info', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='common.contactinfo')),
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
                ('citizenship', models.CharField(max_length=64, null=True)),
                ('permanent_address', models.CharField(max_length=128, null=True)),
                ('surname_genitive', models.CharField(max_length=32)),
                ('name_genitive', models.CharField(max_length=32)),
                ('patronymic_genitive', models.CharField(blank=True, max_length=32)),
                ('status', models.CharField(choices=[('AP', 'абитуриент'), ('ST', 'обучающийся'), ('DE', 'отчислен'), ('GR', 'выпустился')], default='AP', max_length=2)),
                ('birth_info', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='common.birthinfo')),
                ('contact_info', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='common.contactinfo')),
                ('family', models.ManyToManyField(to='common.Relative')),
                ('milgroup', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='lms.milgroup')),
                ('milspecialty', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='lms.milspecialty')),
                ('passport', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='lms.passport')),
                ('photo', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='common.photo')),
                ('recruitment_office', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='lms.recruitmentoffice')),
                ('university_info', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='lms.universityinfo')),
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
                ('type', models.CharField(choices=[('PU', 'Взыскание'), ('RE', 'Выговор')], max_length=2)),
                ('date', models.DateField(default=datetime.date.today)),
                ('remove_date', models.DateField(blank=True, null=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='lms.student')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='lms.teacher')),
            ],
            options={
                'verbose_name': 'Punishment Journal',
                'verbose_name_plural': 'Punishment Journal',
            },
        ),
        migrations.CreateModel(
            name='Mark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mark', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(2)]), size=None)),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='lms.lesson')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='lms.student')),
            ],
            options={
                'verbose_name': 'Mark',
                'verbose_name_plural': 'Marks',
            },
        ),
        migrations.AddField(
            model_name='lesson',
            name='milgroup',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='lms.milgroup'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='lms.room'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='common.subject'),
        ),
        migrations.CreateModel(
            name='Encouragement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(max_length=200)),
                ('type', models.CharField(choices=[('EN', 'Благодарность'), ('RE', 'Снятие взыскания')], max_length=2)),
                ('date', models.DateField(default=datetime.date.today)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='lms.student')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='lms.teacher')),
            ],
            options={
                'verbose_name': 'Encouragement Journal',
                'verbose_name_plural': 'Encouragement Journal',
            },
        ),
        migrations.CreateModel(
            name='Achievement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('date', models.DateField(null=True)),
                ('achievement_type', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='lms.achievementtype')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='lms.student')),
            ],
            options={
                'verbose_name': 'Achievement Journal',
                'verbose_name_plural': 'Achievement Journal',
            },
        ),
        migrations.CreateModel(
            name='Absence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date.today)),
                ('type', models.CharField(choices=[('SE', 'Уважительная'), ('NS', 'Неуважительная'), ('LA', 'Опоздание')], max_length=2)),
                ('status', models.CharField(choices=[('OP', 'Открыт'), ('CL', 'Закрыт')], max_length=2)),
                ('reason', models.CharField(blank=True, max_length=100, null=True)),
                ('comment', models.CharField(blank=True, max_length=100, null=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lms.student')),
            ],
            options={
                'verbose_name': 'Absence Journal',
                'verbose_name_plural': 'Absence Journal',
                'unique_together': {('date', 'student')},
            },
        ),
    ]
