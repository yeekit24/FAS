from django.db.models import QuerySet

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from src.applicants.models import Applicant
from src.common.logic import check_through_schemes
from .models import Scheme, SchemeBenefit, SchemeCriteria
from .serializer import (
    CreateSchemeSerializer,
    EligibleSchemeSerializer,
    SchemeSerializer,
)


class SchemeViewset(viewsets.ModelViewSet):
    serializer_class = SchemeSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self) -> QuerySet[Scheme]:
        query = Scheme.objects.select_related().filter(is_active=True)
        return query

    @swagger_auto_schema(auto_schema=None)
    def destroy(self, request, *args, **kwargs):
        return Response(
            {"detail": 'Method "DELETE" not allowed.'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "applicant",
                in_=openapi.IN_QUERY,
                description="Unique identifier for the applicant",
                type=openapi.TYPE_STRING,
                required=True,
            )
        ],
        responses={
            200: SchemeSerializer(many=True),
            400: "Bad Request",
        },
    )
    @action(detail=False, methods=["get"])
    def eligible(self, request):
        serializer = EligibleSchemeSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        applicant_uid = request.query_params["applicant"]
        applicant = Applicant.objects.get(uid=applicant_uid)
        schemes = self.get_queryset()

        avai_schemes = check_through_schemes(applicant, schemes)
        return Response(
            self.serializer_class(avai_schemes, many=True).data,
            status=status.HTTP_200_OK,
        )

    def create(self, request):
        serializer = CreateSchemeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        input = {**serializer.validated_data}

        benefits = input.pop("benefits")
        criterias = input.pop("criterias")
        scheme = Scheme.objects.create(**input)

        for benefit in benefits:
            SchemeBenefit.objects.create(scheme_id=scheme, **benefit)
        for criteria in criterias:
            SchemeCriteria.objects.create(scheme_id=scheme, **criteria)
        return Response({"uid": scheme.uid}, status=status.HTTP_201_CREATED)
