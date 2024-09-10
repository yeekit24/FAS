import uuid

from rest_framework import serializers

from .models import Application
from src.applicants.serializer import ApplicantSerializer
from src.schemes.serializer import SchemeSerializer

class ApplicationSerializer(serializers.ModelSerializer):
    applicant = ApplicantSerializer()
    scheme = SchemeSerializer()

    class Meta:
        model = Application
        exclude = ["id"]