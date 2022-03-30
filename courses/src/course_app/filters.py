from django.db.models import Count
from django_filters import rest_framework as filters

from course_app.models import Course


class CourseFilter(filters.FilterSet):
    id__in = filters.BaseInFilter(field_name='id')

    title = filters.CharFilter(field_name='title', lookup_expr='icontains')

    starts_at= filters.DateFilter(field_name='starts_at')
    ends_at = filters.DateFilter(field_name='ends_at')

    starts_at_range = filters.DateFromToRangeFilter(field_name='starts_at')
    ends_at_range = filters.DateFromToRangeFilter(field_name='ends_at')

    lectures_more_than = filters.NumberFilter(field_name='lectures', method='filter_amount_of_lectures_more_than')

    ordering = filters.OrderingFilter(
        fields=(
            ('title', 'title'),
            ('starts_at', 'starts_at'),
            ('ends_at', 'ends_at'),
        )
    )

    class Meta:
        model = Course
        fields = ['id', 'title', 'starts_at', 'ends_at']

    def filter_amount_of_lectures_more_than(self, queryset, name, value):
        return queryset.annotate(amount_of_lectures=Count(name))\
            .filter(amount_of_lectures__gte=value)\
            .order_by('-amount_of_lectures')
