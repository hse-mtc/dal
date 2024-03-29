from django.db import models

from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import (
    AbstractUser,
    GroupManager,
    PermissionManager,
)

from common.models.universities import Campus


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


class Permission(models.Model):
    class Scope(models.IntegerChoices):
        ALL = 0, "all"
        MILFACULTY = 10, "milfaculty"
        MILGROUP = 20, "milgroup"
        SELF = 30, "self"

    scope = models.IntegerField(choices=Scope.choices)
    viewset = models.CharField(max_length=100)
    method = models.CharField(max_length=100)

    name = models.CharField(max_length=255)

    objects = PermissionManager()

    @property
    def codename(self):
        return ".".join([self.viewset, self.method, self.get_scope_display()])

    class Meta:
        verbose_name = "Permission"
        verbose_name_plural = "Permissions"

    def __str__(self):
        return self.name


class Group(models.Model):
    permissions = models.ManyToManyField(
        Permission,
        verbose_name="permissions",
        blank=True,
    )
    name = models.CharField("name", max_length=150, unique=True)

    objects = GroupManager()

    class Meta:
        verbose_name = "Group"
        verbose_name_plural = "Groups"

    def __str__(self):
        return self.name


class User(AbstractUser):
    username = None
    first_name = None
    last_name = None
    email = models.EmailField("email address", unique=True)

    campuses = ArrayField(
        base_field=models.CharField(
            max_length=2,
            choices=Campus.choices,
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
        help_text="The groups this user belongs to. A user will get all permissions "
        "granted to each of their groups.",
        related_name="user_set",
        related_query_name="user",
    )

    user_permissions = None  # Remove default ones.
    permissions = models.ManyToManyField(
        Permission,
        verbose_name="user permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        related_name="user_set",
        related_query_name="user",
    )

    # pylint: disable=arguments-differ
    def get_group_permissions(self):
        permissions = Permission.objects.none()
        for group in self.groups.all():
            permissions = permissions.union(group.permissions.all())
        return permissions

    # pylint: disable=arguments-differ
    def get_all_permissions(self):
        return self.permissions.union(self.get_group_permissions())

    def _filter_permissions(self, viewset, method):
        perms = self.get_all_permissions().values()
        # using .filter() is not possible after union
        return [
            perm
            for perm in perms
            if (perm["viewset"] == viewset) and (perm["method"] == method.lower())
        ]

    def has_general_perm(self, viewset, method):
        perms = self._filter_permissions(viewset, method)
        return len(perms) > 0

    def get_perm_scope(self, viewset, method):
        perms = self._filter_permissions(viewset, method)
        return min([p["scope"] for p in perms]) if perms else None

    def __str__(self):
        return self.email
