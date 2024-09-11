from django.db.models import QuerySet
from django.utils import timezone

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from src.applicants.models import Applicant
from src.common.logic import check_through_schemes
from src.schemes.models import Scheme
from src.users.models import User
from .models import Application
from .serializer import (
    ApplicationSerializer,
    CreateApplicationSerializer,
    EligibleApplicationSerializer,
)


class ApplicationViewset(viewsets.ModelViewSet):
    serializer_class = ApplicationSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self) -> QuerySet[Application]:
        params = self.request.query_params
        scheme_uid = params.get("scheme_uid")
        applicant_uid = params.get("applicant_uid")

        query = Application.objects.select_related().filter(is_active=True)
        if scheme_uid:
            query = query.filter(scheme__is_active=True, scheme__uid=scheme_uid)
        if applicant_uid:
            query = query.filter(
                applicant__is_active=True, applicant__uid=applicant_uid
            )
        return query

    @swagger_auto_schema(auto_schema=None)
    def destroy(self, request, *args, **kwargs):
        return Response(
            {"detail": 'Method "DELETE" not allowed.'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def create(self, request):
        serializer = CreateApplicationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        input = {**serializer.validated_data}

        applicant_uid = input.pop("applicant_uid")
        scheme_uid = input.pop("scheme_uid")
        reviewer_uid = input.pop("reviewer")

        applicant = Applicant.objects.get(uid=applicant_uid, is_active=True)
        scheme = Scheme.objects.get(uid=scheme_uid, is_active=True)
        reviewer = User.objects.get(uid=reviewer_uid, is_active=True)
        if not (applicant or scheme or reviewer):
            return Response(status=status.HTTP_404_NOT_FOUND)
        application = Application.objects.create(
            applicant=applicant,
            scheme=scheme,
            reviewer=reviewer,
            created_time=timezone.now(),
            status=Application.Status.PENDING,
            **input
        )
        return Response({"uid": application.uid}, status=status.HTTP_201_CREATED)

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
            200: {"result": "Approved"},
            400: "Bad Request",
        },
    )
    @action(detail=False, methods=["get"])
    def check_eligible(self, request):
        serializer = EligibleApplicationSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        application = Application.objects.select_related().get(
            uid=serializer.validated_data["applicant"], is_active=True
        )

        if not application:
            return Response(status=status.HTTP_404_NOT_FOUND)
        result = (
            Application.Status.APPROVED
            if check_through_schemes(
                applicant=application.applicant, schemes=[application.scheme]
            )
            else Application.Status.REJECTED
        )
        return Response({"result": result}, status=status.HTTP_200_OK)
