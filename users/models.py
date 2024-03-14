from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from core.models import TimeStampedModel


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email, name and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    """User model. This identifies whether the user is an
    account manager, client manager, or admin"""

    class Roles(models.TextChoices):
        ACCOUNT_MANAGER = "ACCOUNT_MANAGER", _("Account Manager")
        CLIENT_MANAGER = "CLIENT_MANAGER", _("Client Manager")
        ADMIN = "ADMIN", _("Admin")

    username = None
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(_("first name"), max_length=30, null=True, blank=True)
    last_name = models.CharField(_("last name"), max_length=30, null=True, blank=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    role = models.CharField(max_length=20, choices=Roles.choices)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = "Users"
        verbose_name_plural = "All Users"

    def __str__(self):
        return self.email


# Model Managers for proxy models


class ACManager(models.Manager):
    # Ensures queries on the Account Manager model return only Account Managers
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(role=User.Roles.ACCOUNT_MANAGER)


class CLManager(models.Manager):
    # Ensures queries on the Client Manager model return only Client Managers
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(role=User.Roles.CLIENT_MANAGER)


class ClientManager(User):
    # This sets the user role to Client Manager during record creation

    base_role = User.Roles.CLIENT_MANAGER
    objects = CLManager()

    # Setting proxy to "True" means a table WILL NOT be created # for this record
    class Meta:
        proxy = True
        verbose_name = "Client Manager"
        verbose_name_plural = "Client Managers"

    def __str__(self):
        return self.email


class AccountManager(User):
    # This sets the user role to Account Manager during record creation
    base_role = User.Roles.ACCOUNT_MANAGER
    objects = ACManager()

    class Meta:
        proxy = True
        verbose_name = "Account Manager"
        verbose_name_plural = "Account Managers"

    def __str__(self):
        return self.email
