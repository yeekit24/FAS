import uuid

from rest_framework import serializers

from .models import Scheme, SchemeBenefit, SchemeCriteria


class CriteriaSerializer(serializers.ModelSerializer):
    uid = serializers.UUIDField(required=False, default=uuid.uuid4)

    class Meta:
        model = SchemeCriteria
        exclude = ["id"]


class BenefitSerializer(serializers.ModelSerializer):
    uid = serializers.UUIDField(required=False, default=uuid.uuid4)

    class Meta:
        model = SchemeBenefit
        exclude = ["id"]


class SchemeSerializer(serializers.ModelSerializer):
    scheme_criteria = CriteriaSerializer(many=True)
    scheme_benefit = BenefitSerializer(many=True)

    class Meta:
        model = Scheme
        exclude = ["id"]

    def update(self, instance, validated_data):
        # Update parent fields
        instance.name = validated_data.get("name", instance.name)
        instance.desc = validated_data.get("desc", instance.desc)
        instance.save()

        # Update or create child objects
        benefits_data = validated_data.get("scheme_benefit", [])
        for benefit_data in benefits_data:
            benefit_uid = benefit_data.get("uid")
            if benefit_uid:
                # Update existing child
                benefit = SchemeBenefit.objects.get(uid=benefit_uid, scheme_id=instance)
                benefit.name = benefit_data.get("name", benefit.name)
                benefit.desc = benefit_data.get("desc", benefit.desc)
                benefit.amount = benefit_data.get("amount", benefit.amount)
                benefit.apply_household = benefit_data.get(
                    "apply_household", benefit.apply_household
                )
                benefit.save()
            else:
                # Create a new child if no ID is provided
                SchemeBenefit.objects.create(scheme_id=instance, **benefit_data)

        # Update or create child objects
        criterias_data = validated_data.get("scheme_criteria", [])
        for criteria_data in criterias_data:
            criteria_uid = criteria_data.get("uid")
            if criteria_uid:
                # Update existing child
                criteria = SchemeCriteria.objects.get(
                    uid=criteria_uid, scheme_id=instance
                )
                criteria.name = criteria_data.get("name", criteria.name)
                criteria.field = criteria_data.get("field", criteria.field)
                criteria.ops = criteria_data.get("ops", criteria.ops)
                criteria.threshold = criteria_data.get("threshold", criteria.threshold)
                criteria.is_or = criteria_data.get("is_or", criteria.is_or)
                criteria.apply_household = criteria_data.get(
                    "apply_household", criteria.apply_household
                )
                criteria.save()
            else:
                # Create a new child if no ID is provided
                SchemeCriteria.objects.create(scheme_id=instance, **criteria_data)
        return instance


class EligibleSchemeSerializer(serializers.ModelSerializer):
    applicant = serializers.UUIDField(required=True)

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
        model = SchemeBenefit
        exclude = ["id", "scheme_id", "is_active", "modified_time"]


class CreateSchemeSerializer(serializers.ModelSerializer):
    criterias = CreateCriteriaSerializer(many=True)
    benefits = CreateBenefitSerializer(many=True)
    uid = serializers.UUIDField(required=False, default=uuid.uuid4)

    class Meta:
        model = Scheme
        exclude = ["id", "is_active", "modified_time"]
