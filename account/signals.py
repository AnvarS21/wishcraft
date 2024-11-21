from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import OTPToken
from core.tasks import send_confirmation_email_task


@receiver(post_save, sender=OTPToken)
def send_otp_email(sender, instance, created, **kwargs):
    """Отправляет OTP токен на email после его создания"""
    if created:
        user_email = instance.user.email
        token = instance.token

        send_confirmation_email_task.delay(user_email, token)
