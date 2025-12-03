# checkin/filters.py

import django_filters
from .models import CheckIn


class CheckInFilter(django_filters.FilterSet):
    # Filter by Employee Name (case-insensitive contains lookup)
    employee_name = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Employee Name Contains'
    )

    # Filter by Employee ID (exact match)
    employee_id = django_filters.CharFilter(
        lookup_expr='exact',
        label='Employee ID'
    )

    # Filter by Submission Date (date range)
    timestamp__gte = django_filters.DateFilter(
        field_name='timestamp',
        lookup_expr='gte',
        label='Start Date (On or After)'
    )

    timestamp__lte = django_filters.DateFilter(
        field_name='timestamp',
        lookup_expr='lte',
        label='End Date (On or Before)'
    )

    class Meta:
        model = CheckIn
        fields = [
            'employee_name',
            'employee_id',
            'company',
            'current_location',
        ]