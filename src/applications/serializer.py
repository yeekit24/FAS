import uuid

from rest_framework import serializers

from src.applicants.serializer import ApplicantSerializer
from src.schemes.serializer import SchemeSerializer
from src.users.serializers import UserSerializer
from .models import Application


class ApplicationSerializer(serializers.ModelSerializer):
    applicant = ApplicantSerializer()
    scheme = SchemeSerializer()
    reviewer = UserSerializer()

    class Meta:
        model = Application
        exclude = ["id"]


class CreateApplicationSerializer(serializers.ModelSerializer):
    uid = serializers.UUIDField(required=False, default=uuid.uuid4)
    applicant_uid = serializers.UUIDField()
    scheme_uid = serializers.UUIDField()
    reviewer = serializers.UUIDField()

    class Meta:
        model = Application
        fields = ["uid", "applicant_uid", "scheme_uid", "reviewer"]


class EligibleApplicationSerializer(serializers.ModelSerializer):
    application = serializers.UUIDField(required=True)

    class Meta:
        model = Application
        fields = ["application"]


class EligibleResultSerializer(serializers.ModelSerializer):
    result = serializers.CharField()

    class Meta:
        model = Application
        fields = ["result"]
