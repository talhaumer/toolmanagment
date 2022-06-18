from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group
from django.db import models
from django.utils.text import slugify

from main.models import Base


class AccessLevel:
    """
    Access levels for user roles.
    """

    ADMIN = 800
    SUPER_ADMIN = 900

    ADMIN_CODE = "admin"
    SUPER_ADMIN_CODE = "super_admin"

    CHOICES = (
        (ADMIN, "Admin"),
        (SUPER_ADMIN, "Super_Admin"),
    )

    CODES = (
        (ADMIN, "admin"),
        (SUPER_ADMIN, "super-admin"),
    )

    DICT = dict(CHOICES)
    CODES_DICT = dict(CODES)


class Role(Base):
    """Role model."""

    name = models.CharField(db_column="Name", max_length=255, unique=True)
    code = models.SlugField(db_column="Code", default="")
    description = models.TextField(db_column="Description", null=True, blank=True)
    access_level = models.IntegerField(
        db_column="AccessLevel",
        choices=AccessLevel.CHOICES,
        default=AccessLevel.ADMIN,
    )

    class Meta:
        db_table = "Roles"

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        try:
            if not self.pk:
                self.code = slugify(self.name)
            super().save()
        except Exception:
            raise

    def get_role_by_code(self=None, code=None):
        try:
            return Role.objects.get(code__exact=code)
        except Exception as e:
            print(e)
            return e


class CustomAccountManager(BaseUserManager):
    def create_user(self, email, password):
        user = self.model(email=email, password=password)
        user.role = Role.objects.get(code="super_admin")
        user.set_password(password)
        user.is_superuser = False
        user.is_approved = False
        user.is_active = False
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(email=email, password=password)
        user.is_superuser = True
        user.is_approved = True
        user.is_active = True
        user.role = Role.objects.get(code="super_admin")
        user.save()
        return user


class User(AbstractBaseUser, Base, PermissionsMixin):
    """User model."""

    first_name = models.CharField(db_column="Name", default="", max_length=255)
    last_name = models.CharField(db_column="Address", default="", max_length=255)
    username = models.CharField(db_column="Phone", default="", max_length=255)
    is_active = models.BooleanField(
        db_column="IsActive",
        default=True,
        help_text="Designates whether this user should be treated as active.",
    )
    email = models.EmailField(unique=True, db_column="Email", help_text="Email Field")
    # image = models.ImageField(
    #     upload_to="uploads/", db_column="ImageField", null=True, blank=True
    # )
    is_approved = models.BooleanField(
        db_column="IsApproved",
        default=False,
        help_text="Designates whether this user is approved or not.",
    )
    is_staff = models.BooleanField(
        default=True,
        help_text="Designates whether the user can log into this admin site.",
    )
    role = models.ForeignKey(
        Role,
        db_column="RoleId",
        related_name="user_role",
        on_delete=models.CASCADE,
        default=None,
    )

    objects = CustomAccountManager()
    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"

    class Meta:
        db_table = "User"

    def save(self, *args, **kwargs):
        try:
            if not self.pk:
                self.email = self.email.replace(" ", "").lower()
            super().save()
        except Exception:
            raise


