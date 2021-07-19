# Generated by Django 3.2.3 on 2021-07-16 09:35

import datetime
from django.conf import settings
import django.contrib.postgres.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('common', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AbsenceTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('absence_restriction_time', models.TimeField()),
            ],
            options={
                'verbose_name': 'Absence Time',
                'verbose_name_plural': 'Absence Time',
            },
        ),
        migrations.CreateModel(
            name='AchievementType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'verbose_name': 'Achievement Type',
                'verbose_name_plural': 'Achievement Types',
            },
        ),
        migrations.CreateModel(
            name='ApplicationProcess',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medical_examination', models.CharField(blank=True, choices=[('FI', 'годен'), ('FMR', 'годен с незначительными ограничениями'), ('FLI', 'ограниченно годен'), ('UR', 'ограниченно не годен'), ('UN', 'не годен')], max_length=3)),
                ('prof_psy_selection', models.CharField(blank=True, choices=[('FI', 'I'), ('SE', 'II'), ('TH', 'III'), ('FO', 'IV')], max_length=2)),
                ('preferential_right', models.BooleanField(default=False)),
                ('characteristic_handed_over', models.BooleanField(default=False)),
                ('criminal_record_handed_over', models.BooleanField(default=False)),
                ('passport_handed_over', models.BooleanField(default=False)),
                ('registration_certificate_handed_over', models.BooleanField(default=False)),
                ('university_card_handed_over', models.BooleanField(default=False)),
                ('application_handed_over', models.BooleanField(default=False)),
                ('mean_grade', models.DecimalField(decimal_places=2, default=0, max_digits=4, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
            ],
            options={
                'verbose_name': 'Application Process',
                'verbose_name_plural': 'Application Processes',
            },
        ),
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=127, unique=True)),
            ],
            options={
                'verbose_name': 'Faculty',
                'verbose_name_plural': 'Faculties',
            },
        ),
        migrations.CreateModel(
            name='Milfaculty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=127, unique=True)),
                ('abbreviation', models.CharField(max_length=31)),
            ],
            options={
                'verbose_name': 'Military Faculty',
                'verbose_name_plural': 'Military Faculties',
            },
        ),
        migrations.CreateModel(
            name='Milgroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=31, unique=True)),
                ('weekday', models.SmallIntegerField()),
                ('archived', models.BooleanField(default=False)),
                ('milfaculty', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='lms.milfaculty')),
            ],
            options={
                'verbose_name': 'Military Group',
                'verbose_name_plural': 'Military Groups',
            },
        ),
        migrations.CreateModel(
            name='Milspecialty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('code', models.CharField(max_length=31, unique=True)),
                ('available_for', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('MO', 'Москва'), ('SP', 'Санкт-Петербург'), ('NN', 'Нижний Новгород'), ('PE', 'Пермь')], max_length=2), size=None)),
            ],
            options={
                'verbose_name': 'Military Specialty',
                'verbose_name_plural': 'Military Specialties',
            },
        ),
        migrations.CreateModel(
            name='Passport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=8, unique=True)),
                ('title', models.CharField(blank=True, max_length=127, null=True)),
                ('faculty', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='lms.faculty')),
            ],
            options={
                'verbose_name': 'Educational Program',
                'verbose_name_plural': 'Educational Programs',
            },
        ),
        migrations.CreateModel(
            name='Rank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=63, unique=True)),
            ],
            options={
                'verbose_name': 'Military Rank',
                'verbose_name_plural': 'Military Ranks',
            },
        ),
        migrations.CreateModel(
            name='RecruitmentOffice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255)),
                ('city', models.CharField(blank=True, max_length=127)),
                ('district', models.CharField(blank=True, max_length=127)),
            ],
            options={
                'verbose_name': 'Recruitment Office',
                'verbose_name_plural': 'Recruitment Offices',
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=63, unique=True)),
            ],
            options={
                'verbose_name': 'Room',
                'verbose_name_plural': 'Rooms',
            },
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'verbose_name': 'Skill',
                'verbose_name_plural': 'Skills',
            },
        ),
        migrations.CreateModel(
            name='UniversityInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('campus', models.CharField(choices=[('MO', 'Москва'), ('SP', 'Санкт-Петербург'), ('NN', 'Нижний Новгород'), ('PE', 'Пермь')], max_length=2)),
                ('group', models.CharField(max_length=32)),
                ('card_id', models.CharField(max_length=32)),
                ('program', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='lms.program')),
            ],
            options={
                'verbose_name': 'University Info',
                'verbose_name_plural': 'University Infos',
            },
        ),
        migrations.CreateModel(
            name='Uniform',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('headdress', models.CharField(choices=[('CA', 'Кепка'), ('HA', 'Шапка')], max_length=2)),
                ('outerwear', models.CharField(choices=[('PC', 'Бушлат'), ('JA', 'Китель')], max_length=2)),
                ('gloves', models.BooleanField(default=False)),
                ('scarf', models.BooleanField(default=False)),
                ('milfaculty', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='lms.milfaculty')),
            ],
            options={
                'verbose_name': 'Current uniform',
                'verbose_name_plural': 'Current uniforms',
            },
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surname', models.CharField(max_length=32)),
                ('name', models.CharField(max_length=32)),
                ('patronymic', models.CharField(blank=True, max_length=32)),
                ('citizenship', models.CharField(blank=True, max_length=64)),
                ('permanent_address', models.CharField(blank=True, max_length=128)),
                ('surname_genitive', models.CharField(max_length=32)),
                ('name_genitive', models.CharField(max_length=32)),
                ('patronymic_genitive', models.CharField(blank=True, max_length=32)),
                ('post', models.CharField(blank=True, choices=[('CH', 'начальник ВУЦ'), ('FH', 'начальник цикла'), ('TE', 'профессорско-преподавательский состав')], default='TE', max_length=2, null=True)),
                ('birth_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='common.birthinfo')),
                ('contact_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='common.contactinfo')),
                ('milfaculty', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='lms.milfaculty')),
                ('milgroups', models.ManyToManyField(blank=True, to='lms.Milgroup')),
                ('photo', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='common.photo')),
                ('rank', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='lms.rank')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Teacher',
                'verbose_name_plural': 'Teachers',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surname', models.CharField(max_length=32)),
                ('name', models.CharField(max_length=32)),
                ('patronymic', models.CharField(blank=True, max_length=32)),
                ('citizenship', models.CharField(blank=True, max_length=64)),
                ('permanent_address', models.CharField(blank=True, max_length=128)),
                ('surname_genitive', models.CharField(max_length=32)),
                ('name_genitive', models.CharField(max_length=32)),
                ('patronymic_genitive', models.CharField(blank=True, max_length=32)),
                ('status', models.CharField(choices=[('AP', 'абитуриент'), ('ST', 'обучающийся'), ('EX', 'отчислен'), ('GR', 'выпустился'), ('AW', 'в ожидании'), ('DE', 'отклонен')], default='AP', max_length=2)),
                ('post', models.CharField(blank=True, choices=[('GC', 'командир взвода'), ('SC', 'командир отделения')], default=None, max_length=2, null=True)),
                ('application_process', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='lms.applicationprocess')),
                ('birth_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='common.birthinfo')),
                ('contact_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='common.contactinfo')),
                ('family', models.ManyToManyField(blank=True, to='common.Relative')),
                ('milgroup', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='lms.milgroup')),
                ('milspecialty', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='lms.milspecialty')),
                ('passport', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='lms.passport')),
                ('photo', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='common.photo')),
                ('recruitment_office', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='lms.recruitmentoffice')),
                ('skills', models.ManyToManyField(blank=True, to='lms.Skill')),
                ('university_info', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='lms.universityinfo')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Student',
                'verbose_name_plural': 'Students',
            },
        ),
        migrations.CreateModel(
            name='Punishment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('PU', 'Взыскание'), ('RE', 'Выговор')], max_length=2)),
                ('reason', models.CharField(max_length=200)),
                ('date', models.DateField(default=datetime.date.today)),
                ('remove_date', models.DateField(blank=True, null=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lms.student')),
                ('teacher', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='lms.teacher')),
            ],
            options={
                'verbose_name': 'Punishment Journal',
                'verbose_name_plural': 'Punishment Journal',
            },
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lms.student')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Note',
                'verbose_name_plural': 'Notes',
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('LE', 'Лекция'), ('SE', 'Семинар'), ('GR', 'Групповое занятие'), ('PR', 'Практическое занятие'), ('FI', 'Зачет'), ('EX', 'Экзамен')], max_length=2)),
                ('date', models.DateField(default=datetime.date.today)),
                ('ordinal', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(10), django.core.validators.MinValueValidator(1)])),
                ('milgroup', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='lms.milgroup')),
                ('room', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='lms.room')),
                ('subject', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.subject')),
                ('teacher', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='lms.teacher')),
            ],
            options={
                'verbose_name': 'Lesson',
                'verbose_name_plural': 'Lessons',
            },
        ),
        migrations.CreateModel(
            name='Encouragement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('EN', 'благодарность'), ('RE', 'снятие взыскания')], max_length=2)),
                ('reason', models.CharField(max_length=255)),
                ('date', models.DateField(default=datetime.date.today)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lms.student')),
                ('teacher', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='lms.teacher')),
            ],
            options={
                'verbose_name': 'Encouragement Journal',
                'verbose_name_plural': 'Encouragement Journal',
            },
        ),
        migrations.CreateModel(
            name='Achievement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('date', models.DateField(blank=True, null=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lms.student')),
                ('type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='lms.achievementtype')),
            ],
            options={
                'verbose_name': 'Achievement Journal',
                'verbose_name_plural': 'Achievement Journal',
            },
        ),
        migrations.CreateModel(
            name='Mark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('values', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(2)]), size=None)),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lms.lesson')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lms.student')),
            ],
            options={
                'verbose_name': 'Mark',
                'verbose_name_plural': 'Marks',
                'unique_together': {('lesson', 'student')},
            },
        ),
        migrations.CreateModel(
            name='Absence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('excuse', models.CharField(choices=[('LA', 'Опоздание'), ('LE', 'Уважительная'), ('IL', 'Неуважительная')], max_length=2)),
                ('status', models.CharField(choices=[('OP', 'Открыт'), ('CL', 'Закрыт')], max_length=2)),
                ('date', models.DateField(default=datetime.date.today)),
                ('reason', models.CharField(blank=True, max_length=127, null=True)),
                ('comment', models.CharField(blank=True, max_length=127, null=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lms.student')),
            ],
            options={
                'verbose_name': 'Absence Journal',
                'verbose_name_plural': 'Absence Journal',
                'unique_together': {('date', 'student')},
            },
        ),
    ]
