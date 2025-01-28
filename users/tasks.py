from datetime import timedelta

from celery import shared_task
from django.utils.timezone import now

from users.models import EmailVerification, User


@shared_task
def send_email_verification(user_id):
    record = EmailVerification.objects.create(expire_at=now() + timedelta(hours=48), user=User.objects.get(pk=user_id))
    record.send_verification_email()
