import uuid

from rest_framework import serializers

from .models import Scheme, SchemeBenefits, SchemeCriteria


class CriteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchemeCriteria
        exclude = ["id"]


class BenefitSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchemeBenefits
        exclude = ["id"]


class SchemeSerializer(serializers.ModelSerializer):
    scheme_criteria = CriteriaSerializer(many=True)
    scheme_benefit = BenefitSerializer(many=True)

    class Meta:
        model = Scheme
        exclude = ["id"]


class CreateCriteriaSerializer(serializers.ModelSerializer):
    uid = serializers.UUIDField(required=False, default=uuid.uuid4)

    class Meta:
        model = SchemeCriteria
        exclude = ["id", "scheme_id", "is_active", "modified_time"]


class CreateBenefitSerializer(serializers.ModelSerializer):
    uid = serializers.UUIDField(required=False, default=uuid.uuid4)

    class Meta:
        model = SchemeBenefits
        exclude = ["id", "scheme_id", "is_active", "modified_time"]


class CreateSchemeSerializer(serializers.ModelSerializer):
    criterias = CreateCriteriaSerializer(many=True)
    benefits = CreateBenefitSerializer(many=True)
    uid = serializers.UUIDField(required=False, default=uuid.uuid4)

    class Meta:
        model = Scheme
        exclude = ["id", "is_active", "modified_time"]
