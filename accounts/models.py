from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    # CREATE BASIC USER
    def create_user(self, username, email, password=None, **extra_fields):
        # STANDARDIZE THE EMAIL FORMAT BEFORE STORING IT IN THE DATABASE
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)

        # CUSTOM PASSWORD STORAGE LOGIC
        user.set_password(password)
        user.save(using=self._db)

        return user

    # CREATE ADMIN USER
    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        return self.create_user(username, email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    # USER PERSONAL DATA
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    # USE EMAIL FIELD AS AN AUTHENTIFICATION FIELD
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # GETTERS FOR EMAIL AND FULL NAME OF THE USER
    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def clean_password(self, raw_password):
        # PASSWORD STRENGTH VALIDATION
        if validate_password(raw_password, user=self.user):
            return raw_password
        else:
            raise ValidationError("Password is Unvalid")
