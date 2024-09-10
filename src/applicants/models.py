import uuid
from django.db import models
from django.utils import timezone
from src.common.models.base import BaseModel

class Applicant(BaseModel):
    class EmploymentStatus(models.TextChoices):
        UNEMPLOYED ="unemployed"
        EMPLOYED="employed"

    class MaritalStatus(models.TextChoices):
        SINGLE="single"
        MARRIED="married"
        WIDOWED="widowed"
        DIVORCED="divorced"

    class Sex(models.TextChoices):
        M="male"
        F="female"

    uid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
    )
    name = models.CharField(max_length=255, null=True, blank=True)
    date_of_birth=models.DateField(blank=True, null=True)
    marital_status=models.CharField(choices=MaritalStatus.choices, max_length=20)
    employment_status = models.CharField(choices=EmploymentStatus.choices, max_length=50)
    sex = models.CharField(choices=Sex.choices, max_length=10, null=True, blank=True)

class ApplicantHousehold(BaseModel):
    class Relationship(models.TextChoices):
        MOTHER="mother"
        FATHER="father"
        SON="son"
        DAUGTHER="daughter"
    
    name = models.CharField(max_length=255, null=True, blank=True)
    date_of_birth=models.DateField(blank=True, null=True)
    marital_status=models.CharField(choices=Applicant.MaritalStatus.choices, max_length=20, default=Applicant.MaritalStatus.SINGLE)
    employment_status = models.CharField(choices=Applicant.EmploymentStatus.choices, max_length=50, default=Applicant.EmploymentStatus.UNEMPLOYED)
    sex = models.CharField(choices=Applicant.Sex.choices, max_length=10, null=True, blank=True)
    applicant_id = models.ForeignKey(Applicant, related_name='households', on_delete=models.PROTECT)
    relation = models.CharField(choices=Relationship.choices, max_length=50)