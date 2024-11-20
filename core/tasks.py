from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_confirmation_email_task(email, token):
    subject = f"Активируйте аккаунт"
    message = f"Ваш одноразовый код: {token}. Используйте его для завершения операции."
    from_email = settings.EMAIL_HOST_USER
    print(message, email, from_email)
    try:
        send_mail(subject, message, from_email, [email])
    except Exception as e:
        print(e, '###########')
    print('!!!!!!!!!!!!!!')
