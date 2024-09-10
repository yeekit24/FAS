from django.db.models import QuerySet

from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination

from .models import Scheme
from .serializer import SchemeSerializer


class SchemeViewset(viewsets.ModelViewSet):
    serializer_class = SchemeSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self) -> QuerySet[Scheme]:
        query = Scheme.objects.select_related().filter(is_active=True)
        return query

    def eligible(self):
        pass
        #request.query_params
        query = Scheme.objects.select_related()
