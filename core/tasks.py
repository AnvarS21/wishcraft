from celery import shared_task

@shared_task
def send_confirmation_email_task(account):
    pass