"""Authentication signals module."""
from django.db.models.signals import post_save
from django.dispatch import receiver

from rest_framework.authtoken.models import Token

from src.users.models import User


@receiver(post_save, sender=User)
def create_auth_token(sender, raw, instance=None, created=False, **kwargs):
    # Don't trigger signal on fixture loading.
    if created and not raw:
        Token.objects.create(user=instance)
