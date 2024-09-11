import uuid
from django.db import models
from django.utils import timezone

from src.common.models.base import BaseModel


class ParentApplicant(BaseModel):
    class EmploymentStatus(models.TextChoices):
        UNEMPLOYED = "unemployed"
        EMPLOYED = "employed"

    class MaritalStatus(models.TextChoices):
        SINGLE = "single"
        MARRIED = "married"
        WIDOWED = "widowed"
        DIVORCED = "divorced"

    class Sex(models.TextChoices):
        M = "male"
        F = "female"

    uid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(max_length=255, null=True, blank=True)
    date_of_birth = models.DateField()
    marital_status = models.CharField(choices=MaritalStatus.choices, max_length=20)
    employment_status = models.CharField(
        choices=EmploymentStatus.choices, max_length=50
    )
    sex = models.CharField(choices=Sex.choices, max_length=10)

    class Meta:
        abstract = True

    def get_age(self):
        today = timezone.now().date()
        age = today.year - self.date_of_birth.year
        if today.month < self.date_of_birth.month or (
            today.month == self.date_of_birth.month
            and today.day < self.date_of_birth.day
        ):
            age -= 1
        return age


class Applicant(ParentApplicant):
    pass


class ApplicantHousehold(ParentApplicant):
    class Relationship(models.TextChoices):
        MOTHER = "mother"
        FATHER = "father"
        SON = "son"
        DAUGTHER = "daughter"

    applicant_id = models.ForeignKey(
        Applicant, related_name="households", on_delete=models.CASCADE
    )
    relation = models.CharField(choices=Relationship.choices, max_length=50)
