# Generated by Django 3.2.9 on 2021-11-06 18:46

import django.contrib.auth.models
import django.contrib.postgres.fields
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scope', models.IntegerField(choices=[(0, 'all'), (10, 'milfaculty'), (20, 'milgroup'), (30, 'self')])),
                ('viewset', models.CharField(max_length=100)),
                ('method', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Permission',
                'verbose_name_plural': 'Permissions',
            },
            managers=[
                ('objects', django.contrib.auth.models.PermissionManager()),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='name')),
                ('permissions', models.ManyToManyField(blank=True, to='dal_auth.Permission', verbose_name='permissions')),
            ],
            options={
                'verbose_name': 'Group',
                'verbose_name_plural': 'Groups',
            },
            managers=[
                ('objects', django.contrib.auth.models.GroupManager()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email address')),
                ('campuses', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('MO', 'Москва'), ('SP', 'Санкт-Петербург'), ('NN', 'Нижний Новгород'), ('PE', 'Пермь')], max_length=2), default=list, size=None)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='dal_auth.Group', verbose_name='groups')),
                ('permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='dal_auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
    ]
