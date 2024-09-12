import uuid

from rest_framework import serializers

from .models import Applicant, ApplicantHousehold


class ApplicantHouseholdSerializer(serializers.ModelSerializer):
    uid = serializers.UUIDField(required=False, default=uuid.uuid4)

    class Meta:
        model = ApplicantHousehold
        exclude = ["id"]


class ApplicantSerializer(serializers.ModelSerializer):
    households = ApplicantHouseholdSerializer(many=True)

    class Meta:
        model = Applicant
        exclude = ["id"]

    def update(self, instance, validated_data):
        # Update parent fields
        instance.name = validated_data.get("name", instance.name)
        instance.employment_status = validated_data.get(
            "employment_status", instance.employment_status
        )
        instance.sex = validated_data.get("sex", instance.sex)
        instance.date_of_birth = validated_data.get(
            "date_of_birth", instance.date_of_birth
        )
        instance.marital_status = validated_data.get(
            "marital_status", instance.marital_status
        )
        instance.save()

        # Update or create child objects
        households_data = validated_data.get("households", [])
        for household_data in households_data:
            household_uid = household_data.get("uid")
            if household_uid:
                # Update existing child
                household = ApplicantHousehold.objects.get(
                    uid=household_uid, applicant_id=instance
                )
                household.name = household_data.get("name", household.name)
                household.employment_status = household_data.get(
                    "employment_status", household.employment_status
                )
                household.sex = household_data.get("sex", household.sex)
                household.date_of_birth = household_data.get(
                    "date_of_birth", household.date_of_birth
                )
                household.marital_status = household_data.get(
                    "marital_status", household.marital_status
                )
                household.save()
            else:
                # Create a new child if no ID is provided
                ApplicantHousehold.objects.create(
                    applicant_id=instance, **household_data
                )

        return instance


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
