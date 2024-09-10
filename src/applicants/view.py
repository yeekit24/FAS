from django.db.models import QuerySet

from rest_framework import status, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from .models import Applicant, ApplicantHousehold
from .serializer import ApplicantSerializer, CreateApplicantSerializer


class ApplicantViewset(viewsets.ModelViewSet):
    serializer_class = ApplicantSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self) -> QuerySet[Applicant]:
        query = Applicant.objects.select_related().filter(is_active=True)
        return query

    def create(self, request):
        serializer = CreateApplicantSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        input = {**serializer.validated_data}

        households = input.pop("households")
        applicant = Applicant.objects.create(**input)

        for household in households:
            ApplicantHousehold.objects.create(applicant_id=applicant, **household)

        return Response({"uid": applicant.uid}, status=status.HTTP_201_CREATED)
