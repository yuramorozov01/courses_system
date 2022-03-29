from django_filters import rest_framework as filters

from course_app.models import Course


class CourseFilter(filters.FilterSet):
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')
    starts_at_after = filters.DateFilter(field_name='starts_at', lookup_expr='gte')
    ends_at_before = filters.DateFilter(field_name='ends_at', lookup_expr='lte')

    ordering = filters.OrderingFilter(
        fields=(
            ('title', 'title'),
        )
    )

    class Meta:
        model = Course
        fields = ['title', 'starts_at', 'ends_at']
