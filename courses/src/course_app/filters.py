from django_filters import rest_framework as filters

from course_app.models import Course


class CourseFilter(filters.FilterSet):
    id__in = filters.BaseInFilter(field_name='id')

    title = filters.CharFilter(field_name='title', lookup_expr='icontains')

    starts_at= filters.DateFilter(field_name='starts_at')
    ends_at = filters.DateFilter(field_name='ends_at')

    starts_at_range = filters.DateFromToRangeFilter(field_name='starts_at')
    ends_at_range = filters.DateFromToRangeFilter(field_name='ends_at')

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
