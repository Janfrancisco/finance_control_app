from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    avatar = models.ImageField("Avatar", upload_to="avatars", blank=True, null=True)
    full_name = models.CharField("Nome completo", max_length=200)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "username",
        "full_name",
    ]

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        self.full_name = self.full_name.title()
        name_splited = self.full_name.split()
        self.first_name = name_splited[0]
        self.last_name = name_splited[-1]
        super().save(*args, **kwargs)
