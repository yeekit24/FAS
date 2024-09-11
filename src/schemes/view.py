from django.db.models import QuerySet

from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from src.applicants.models import Applicant
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

    @action(detail=False, methods=["get"])
    def eligible(self, request):
        serializer = EligibleSchemeSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        applicant_uid = request.query_params["applicant"]
        applicant = Applicant.objects.get(uid=applicant_uid)
        schemes = self.get_queryset()

        avai_schemes = []
        for scheme in schemes:
            eli_result = []
            is_all_pass = True
            for criteria in scheme.scheme_criteria.all():
                if criteria.apply_household:
                    if len(applicant.households.all()) == 0:
                        is_all_pass = False
                        break
                    for household in applicant.households.all():
                        if criteria.is_or:
                            eli_result.append(self.is_eligible(criteria, household))
                        else:
                            if not self.is_eligible(criteria, household):
                                is_all_pass = False
                                break
                else:
                    if criteria.is_or:
                        eli_result.append(self.is_eligible(criteria, applicant))
                    else:
                        if not self.is_eligible(criteria, applicant):
                            is_all_pass = False
                            break
            print(f"Scheme {scheme.name} eligible: {is_all_pass} and {any(eli_result)}")
            if is_all_pass and any(eli_result):
                avai_schemes.append(scheme)
        return Response(
            self.serializer_class(avai_schemes, many=True).data,
            status=status.HTTP_200_OK,
        )

    def is_eligible(self, criteria, applicant) -> bool:
        if criteria.field == "employment_status":
            return self.validate(criteria, applicant.employment_status)
        elif criteria.field == "age":
            return self.validate(criteria, applicant.get_age())
        elif criteria.field == "sex":
            return self.validate(criteria, applicant.sex)
        elif criteria.field == "marital_status":
            return self.validate(criteria, applicant.marital_status)
        return True

    def validate(self, criteria, field: str):
        if criteria.ops == SchemeCriteria.OPS.GR:
            return field > float(criteria.threshold)
        elif criteria.ops == SchemeCriteria.OPS.GR_EQ:
            return field >= float(criteria.threshold)
        elif criteria.ops == SchemeCriteria.OPS.LS:
            return field < float(criteria.threshold)
        elif criteria.ops == SchemeCriteria.OPS.LS_EQ:
            return field <= float(criteria.threshold)
        elif criteria.ops == SchemeCriteria.OPS.EQ:
            return field == criteria.threshold
        elif criteria.ops == SchemeCriteria.OPS.IN_:
            return field in (criteria.threshold)

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
