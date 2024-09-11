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
    class OPS(models.TextChoices):
        GR = ">"
        GR_EQ = ">="
        LS = "<"
        LS_EQ = "<="
        EQ = "="
        IN_ = "in"

    class FIELD(models.TextChoices):
        EMPLOYMENT_STATUS = "employment_status"
        SEX = "sex"
        AGE = "age"
        MARITAL_STATUS = "marital_status"

    uid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
    )
    scheme_id = models.ForeignKey(
        Scheme, related_name="scheme_criteria", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    field = models.CharField(choices=FIELD.choices, max_length=255)
    ops = models.CharField(choices=OPS.choices, max_length=2)
    threshold = models.CharField(max_length=255)
    apply_household = models.BooleanField(default=False)
    is_or = models.BooleanField(default=False)


class SchemeBenefit(BaseModel):
    uid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(max_length=100, null=True, blank=True)
    desc = models.TextField(null=True, blank=True)
    amount = models.FloatField()
    scheme_id = models.ForeignKey(
        Scheme, related_name="scheme_benefit", on_delete=models.PROTECT
    )
    apply_household = models.BooleanField(default=False)
