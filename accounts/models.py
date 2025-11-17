from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
import os
import hashlib


class CustomUserManager(BaseUserManager):
    # CREATE BASIC USER
    def create_user(self, email, password=None, **extra_fields):
        # STANDARDIZE THE EMAIL FORMAT BEFORE STORING IT IN THE DATABASE
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        # CUSTOM PASSWORD STORAGE LOGIC
        user.set_password(password)
        user.save(using=self._db)

        return user

    # CREATE ADMIN USER
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    # USER PERSONAL DATA
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # PASSWORD DATA
    salt = models.CharField(max_length=32, editable=False)
    password = models.CharField(max_length=128)

    objects = CustomUserManager()

    # USE EMAIL FIELD AS AN AUTHENTIFICATION FIELD
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # GETTERS FOR EMAIL AND FULL NAME OF THE USER
    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    # PASSWORD CREATION LOGIC
    def set_password(self, raw_password):
        salt = os.urandom(16)
        hashed = hashlib.pbkdf2_hmac(
            'sha256',
            raw_password.encode(),
            salt,
            10000
        )
        self.salt = salt.hex()
        self.password = hashed.hex()

    # PASSWORD VERIFICATION LOGIC
    def check_password(self, raw_password):
        salt = bytes.fromhex(self.salt)
        hashed = hashlib.pbkdf2_hmac(
            'sha256',
            raw_password.encode(),
            salt,
            10000
        )
        return self.password == hashed.hex()
