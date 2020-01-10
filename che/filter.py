from django.db import models
from .models import Cheque
import django_filters


class ChequeFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Cheque
        fields = ['no_cheque', 'fecha_creado']
