from rest_framework import permissions, viewsets
from course_app.serializers import CourseCreateSerializer
from course_app.models import Course


class CourseViewSet(viewsets.ModelViewSet):
    '''
    create:
        Create a new course.

    destroy:
        Delete a Course.
        Only author can delete this ticket.
    '''

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        querysets_dict = {
            'create': Course.objects.filter(author=self.request.user.id),
            'destroy': Course.objects.filter(author=self.request.user.id),
        }
        queryset = querysets_dict.get(self.action)
        return queryset

    def get_serializer_class(self):
        serializers_dict = {
            'create': CourseCreateSerializer,
        }
        serializer_class = serializers_dict.get(self.action)
        return serializer_class

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, teachers=(self.request.user,))
