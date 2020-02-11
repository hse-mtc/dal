from django.apps import AppConfig


class BackendConfig(AppConfig):
    name = 'backend'
    verbose_name = "Backend for DMS"

    # def ready(self):
    #     from django.contrib.auth import get_user_model
    #     superuser = get_user_model().objects.create_superuser(
    #         username="vspelyak",
    #         email="",
    #         password="qwerty",
    #     )
    #
    #     from .models import Profile
    #     profile = Profile(
    #         name="Пеляк В.С.",
    #         user=superuser,
    #     )
    #     profile.save()
