# journal/api/filters.py
import django_filters
from journal.models import Quote

class QuoteFilter(django_filters.FilterSet):
    date_from = django_filters.DateFilter(field_name='created_at', lookup_expr='gte')
    date_to   = django_filters.DateFilter(field_name='created_at', lookup_expr='lte')
    author    = django_filters.NumberFilter(field_name='book__author__id')
    genre     = django_filters.NumberFilter(field_name='book__genre__id')

    class Meta:
        model  = Quote
        fields = ['author', 'genre', 'date_from', 'date_to']
