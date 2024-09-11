# from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    uid = models.UUIDField(
        "UUID",
        default=uuid.uuid4,
        editable=False,
        help_text="User facing ticket ID",
    )
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    modified_time = models.DateTimeField(default=timezone.now)
