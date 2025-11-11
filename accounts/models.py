from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
import os
import hashlib


class CustomUserManager(BaseUserManager):
    # Create Basic User
    def create_user(self, email, password=None, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    # Create Admin user
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    # User Personal data
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # Password data
    salt = models.CharField(max_length=32, editable=False)
    password = models.CharField(max_length=128)

    objects = CustomUserManager()

    # Use email field as an authentification field
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # Getters for email and full name of the user
    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    # Overridden password creation and verification logic
    def set_password(self, raw_password):
        salt = os.urandom(16)
        hashed = hashlib.pbkdf2_hmac('sha256',
                                     raw_password.encode(), salt,
                                     100000)
        self.salt = salt.hex()
        self.password = hashed.hex()

    def check_password(self, raw_password):
        hashed = hashlib.sha256((self.salt + raw_password).encode()).hexdigest()
        return self.password == hashed
