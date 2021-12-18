from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from course_app.serializers import CourseCreateSerializer, CourseDetailsSerializer, CourseShortDetailsSerializer
from course_app.models import Course


class CourseViewSet(viewsets.ModelViewSet):
    '''
    create:
        Create a new course.

    destroy:
        Delete a Course.
        Only author can delete this ticket.

    retrieve:
        Get the specified course.

    list:
        Get a list of all courses.

    update:
        Update a course.
        Author can update the whole course.
        Teachers can add user as a teacher or a student to course.
    '''

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        querysets_dict = {
            'create': Course.objects.filter(author=self.request.user.id),
            'destroy': Course.objects.filter(author=self.request.user.id),
            'retrieve': Course.objects.all(),
            'list': Course.objects.all(),
            # 'update': Course.objects.filter(author=self.request.user.id),
        }
        queryset = querysets_dict.get(self.action)
        return queryset

    def get_serializer_class(self):
        serializers_dict = {
            'create': CourseCreateSerializer,
            'retrieve': CourseDetailsSerializer,
            'list': CourseShortDetailsSerializer,
        }
        serializer_class = serializers_dict.get(self.action)
        return serializer_class

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.id, teachers=(self.request.user.id,))

    @action(methods=['GET'], detail=False)
    def teaching(self, request):
        queryset = Course.objects.filter(teachers=self.request.user.id)
        serializer = CourseShortDetailsSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=False)
    def studying(self, request):
        queryset = Course.objects.filter(students=self.request.user.id)
        serializer = CourseShortDetailsSerializer(queryset, many=True)
        return Response(serializer.data)
