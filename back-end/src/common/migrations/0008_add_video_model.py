# Generated migration for Video model

import uuid
from django.db import migrations, models
import common.models.personal


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0007_add_nationality_graduation_year'),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('file', models.FileField(blank=True, upload_to=common.models.personal.upload_video_to)),
            ],
            options={
                'verbose_name': 'PersonVideo',
                'verbose_name_plural': 'PersonVideos',
            },
        ),
    ]
