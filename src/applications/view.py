from django.db.models import QuerySet

from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from .models import Application
from .serializer import ApplicationSerializer


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
            query = query.filter(applicant__is_active=True, applicant__uid=applicant_uid)
        return query
