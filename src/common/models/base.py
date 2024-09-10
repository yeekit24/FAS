from django.db import models
from django.utils import timezone


class BaseModel(models.Model):
    is_active = models.BooleanField(default=True, db_index=True)
    modified_time = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True
