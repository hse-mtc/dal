# Generated by Django 3.1.7 on 2021-03-19 10:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('common', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surname', models.CharField(max_length=32)),
                ('name', models.CharField(max_length=32)),
                ('patronymic', models.CharField(blank=True, max_length=32)),
                ('citizenship', models.CharField(max_length=64, null=True)),
                ('permanent_address', models.CharField(max_length=128, null=True)),
                ('photo', models.URLField(blank=True)),
                ('birth_info', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='common.birthinfo')),
                ('contact_info', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='common.contactinfo')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Profile',
                'verbose_name_plural': 'Profiles',
            },
        ),
    ]
