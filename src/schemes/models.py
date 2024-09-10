import uuid

from django.db import models

from src.common.models.base import BaseModel

class Scheme(BaseModel):
    uid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(max_length=100, null=True, blank=True)
    desc = models.TextField(null=True, blank=True)

class SchemeCriteria(BaseModel):
    uid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
    )
    scheme_id = models.ForeignKey(Scheme, related_name="scheme_criteria", on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    threshold = models.CharField(max_length=255)

class SchemeBenefits(BaseModel):
    uid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(max_length=100, null=True, blank=True)
    desc = models.TextField(null=True, blank=True)
    amount = models.FloatField()
    scheme_id = models.ForeignKey(Scheme, related_name="scheme_benefit", on_delete=models.PROTECT)