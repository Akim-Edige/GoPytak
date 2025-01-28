import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models


class User(AbstractUser):
    image = models.ImageField(upload_to='users_images', null=True, blank=True)
    is_executor = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    phone = models.CharField(max_length=20, null=True, blank=True)


class EmailVerification(models.Model):
    code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    expire_at = models.DateTimeField()

    def __str__(self):
        return f'Email Verification for {self.user.email}'

    def send_verification_email(self):
        url = f'{settings.DOMAIN_NAME}/users/verify/{self.code}'
        send_mail(
            'Account verification',
            f'Click the link to verify your account:\n\n{url}',
            settings.DEFAULT_FROM_EMAIL,  # Ensure this is set in your settings.py
            [self.user.email],
            fail_silently=False,
        )
