import uuid
from django.db import models

from src.applicants.models import Applicant
from src.common.models.base import BaseModel
from src.schemes.models import Scheme
from src.users.models import User


class Application(BaseModel):
    class Status(models.TextChoices):
        PENDING = "pending"
        APPROVED = "approved"
        REJECTED = "rejected"

    uid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
    )
    applicant = models.ForeignKey(
        Applicant, related_name="applicant_app", on_delete=models.PROTECT
    )
    scheme = models.ForeignKey(
        Scheme, related_name="schem_app", on_delete=models.CASCADE
    )
    created_time = models.DateTimeField()
    status = models.CharField(choices=Status.choices, max_length=100)
    review_date = models.DateTimeField(null=True, blank=True)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
