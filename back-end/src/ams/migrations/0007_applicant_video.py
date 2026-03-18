from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("common", "0008_add_video_model"),
        ("ams", "0006_add_physical"),
    ]

    operations = [
        migrations.AddField(
            model_name="applicant",
            name="video",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=models.deletion.SET_NULL,
                to="common.video",
            ),
        ),
    ]
