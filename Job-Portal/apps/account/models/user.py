from django.contrib.auth.models import AbstractUser
from django.db import models

from account.managers import CustomUserManager

from account.constants import GENDER_TYPE, ROLE, TIPO_EMPRESA


class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True,
        blank=False,
        error_messages={
            'unique': "A user with that email already exists.",
        },
    )
    role = models.CharField(choices=ROLE, max_length=10)
    gender = models.CharField(choices=GENDER_TYPE, max_length=1)
    tipo_empresa = models.CharField(choices=TIPO_EMPRESA, max_length=20, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

