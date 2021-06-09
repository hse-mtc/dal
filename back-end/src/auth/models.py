from django.db import models
from django.contrib.auth.models import (
    AbstractUser, 
    GroupManager,
    PermissionManager,
)
from django.contrib.auth.base_user import BaseUserManager

from django.contrib.postgres.fields import ArrayField


class UserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The Email must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


# FIXME(TmLev): temporary solution. It *should* be imported from
#  `lms.models.universities`, but this may lead to circular import dependency.
#   Anyhow, this must be removed after application process is finished.
class UniversityCampus(models.TextChoices):
    MOSCOW = "MO", "Москва"
    SAINT_PETERSBURG = "SP", "Санкт-Петербург"
    NIZHNY_NOVGOROD = "NN", "Нижний Новгород"
    PERM = "PE", "Пермь"


class User(AbstractUser):
    username = None
    first_name = None
    last_name = None
    email = models.EmailField("email address", unique=True)

    # FIXME(TmLev): should be removed after application process is finished.
    campuses = ArrayField(
        base_field=models.CharField(
            max_length=2,
            choices=UniversityCampus.choices,
        ),
        default=list,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    groups = models.ManyToManyField(
        Group,
        verbose_name="groups",
        blank=True,
        help_text=
            "The groups this user belongs to. A user will get all permissions "
            "granted to each of their groups.",
        related_name="user_set",
        related_query_name="user",
    )
    permissions = models.ManyToManyField(
        Permission,
        verbose_name="user permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        related_name="user_set",
        related_query_name="user",
    )

    def get_group_permissions(self):
        permissions = Permission.objects.none()
        for group in self.groups.all():
            permissions = permissions.union(group.permissions.all())
        return permissions

    def get_all_permissions(self):
        return self.permissions.union(self.get_group_permissions())


    def __str__(self):
        return self.email
