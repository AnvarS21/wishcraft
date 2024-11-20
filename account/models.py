import random
from datetime import timedelta

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from account.managers import UserManager
from django.conf import settings

class User(AbstractUser):
    email = models.EmailField("Почта", unique=True)
    is_active = models.BooleanField(
            "Активность",
            default=False,
            help_text="Указывает, следует ли считать этого пользователя активным"
                      "Снимите этот флажок вместо удаления учетных записей"
    )
    avatar = models.ImageField('Аватар',upload_to='avatars/', null=True, blank=True)


    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Аккаунт"
        verbose_name_plural = "Аккаунты"


    def __str__(self):
        return self.username


class OTPToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='otp_tokens', verbose_name='Пользователь')
    token = models.CharField('Токен', max_length=4)
    purpose = models.CharField('Назначение', max_length=20)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    expires_at = models.DateTimeField('Дата окончания')

    def is_valid(self):
        return now() <= self.expires_at

    def generate_token(self):
        r = random.SystemRandom()

        return str(r.randint(settings.OTP_TOKEN_MIN_NUMBER, settings.OTP_TOKEN_MAX_NUMBER))

    def save(self, *args, **kwargs):
        if not self.pk:
            self.token = self.generate_token()
            self.expires_at = now() + timedelta(minutes=settings.OTP_TOKEN_EXPIRATION_MINUTES)
        super().save(*args, **kwargs)
