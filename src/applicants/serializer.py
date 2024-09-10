import uuid

from rest_framework import serializers
from .models import Applicant, ApplicantHousehold

class ApplicantHouseholdSerializer(serializers.ModelSerializer):

    class Meta:
        model = ApplicantHousehold
        exclude = ["id"]

class ApplicantSerializer(serializers.ModelSerializer):
    households = ApplicantHouseholdSerializer(many=True)

    class Meta:
        model = Applicant
        exclude = ["id"]

class CreateApplicantHouseholdSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicantHousehold
        exclude = ["id", "applicant_id", "is_active", "modified_time"]

class CreateApplicantSerializer(serializers.ModelSerializer):
    households = CreateApplicantHouseholdSerializer(many=True)
    uid = serializers.UUIDField(required=False, default=uuid.uuid4)

    class Meta:
        model = Applicant
        exclude = ["id", "is_active", "modified_time"]