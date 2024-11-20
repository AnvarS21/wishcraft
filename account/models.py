from django.db import models
from django.contrib.auth.models import AbstractUser

from account.managers import UserManager


class User(AbstractUser):
    email = models.EmailField("Почта", unique=True)
    is_active = models.BooleanField(
            "Активность",
            default=False,
            help_text="Указывает, следует ли считать этого пользователя активным"
                      "Снимите этот флажок вместо удаления учетных записей"
    )
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)


    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Аккаунт"
        verbose_name_plural = "Аккаунты"


    def __str__(self):
        return self.username
