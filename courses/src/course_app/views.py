from course_app.filters import CourseFilter
from course_app.models import Course
from course_app.permissions import IsCourseAuthor, IsCourseTeacher
from course_app.serializers import (CourseAddTeachersAndStudentsSerializer,
                                    CourseCreateSerializer,
                                    CourseDetailsSerializer,
                                    CourseShortDetailsSerializer,
                                    CourseUpdateFullSerializer)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


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

    partial_update:
        Add a teacher or a student to a course.
        Teachers can add user as a teacher or a student to course.
    '''

    filterset_class = CourseFilter
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['title', 'lectures__title']

    def get_queryset(self):
        querysets_dict = {
            'create': Course.objects.filter(author=self.request.user.id),
            'destroy': Course.objects.filter(author=self.request.user.id),
            'retrieve': Course.objects.all(),
            'list': Course.objects.all(),
            'update': Course.objects.filter(author=self.request.user.id),
            'partial_update': Course.objects.filter(teachers=self.request.user.id),
            'teaching': Course.objects.filter(teachers=self.request.user.id),
            'studying': Course.objects.filter(students=self.request.user.id),
        }
        queryset = querysets_dict.get(self.action)
        return queryset.distinct()

    def get_serializer_class(self):
        serializers_dict = {
            'create': CourseCreateSerializer,
            'retrieve': CourseDetailsSerializer,
            'list': CourseShortDetailsSerializer,
            'update': CourseUpdateFullSerializer,
            'partial_update': CourseAddTeachersAndStudentsSerializer,
            'teaching': CourseShortDetailsSerializer,
            'studying': CourseShortDetailsSerializer,
        }
        serializer_class = serializers_dict.get(self.action)
        return serializer_class

    def get_permissions(self):
        base_permissions = [permissions.IsAuthenticated]
        permissions_dict = {
            'create': [],
            'destroy': [IsCourseAuthor],
            'retrieve': [],
            'list': [],
            'update': [IsCourseAuthor],
            'partial_update': [IsCourseTeacher],
        }
        base_permissions += permissions_dict.get(self.action, [])
        return [permission() for permission in base_permissions]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, teachers=(self.request.user.id,))

    @action(methods=['GET'], detail=False)
    def teaching(self, request):
        '''Get a list of teaching courses'''
        queryset = self.get_queryset()
        serializer = self.get_serializer_class()(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=False)
    def studying(self, request):
        '''Get a list of studying courses'''
        queryset = self.get_queryset()
        serializer = self.get_serializer_class()(queryset, many=True)
        return Response(serializer.data)
