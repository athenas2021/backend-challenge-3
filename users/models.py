from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.db import models


class User(AbstractUser):
    email = models.EmailField(blank=False, max_length=254, unique=True, verbose_name='email address')


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, username, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email or not username:
            raise ValueError('The given email or username must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password('123456')
        user.save(using=self._db)
        return user

    def create_user(self, email, username, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, username, **extra_fields)

    def create_superuser(self, email, username, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, username, **extra_fields)