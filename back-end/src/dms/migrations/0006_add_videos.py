import datetime

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import dms.models.common


class Migration(migrations.Migration):

    dependencies = [
        ("dms", "0005_alter_category_additional_schema"),
    ]

    operations = [
        migrations.CreateModel(
            name="Video",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.TextField(blank=True)),
                ("annotation", models.TextField(blank=True)),
                ("upload_date", models.DateField(default=datetime.date.today)),
                ("visible_to_students", models.BooleanField(default=True)),
                ("file", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to="dms.file")),
                ("user", models.ForeignKey(default=dms.models.common.super_user_id, on_delete=django.db.models.deletion.SET_DEFAULT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "verbose_name": "Video",
                "verbose_name_plural": "Videos",
            },
        ),
    ]
