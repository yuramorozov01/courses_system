from course_app.choices import StatusChoices
from course_app.models import Course
from course_app.permissions import IsCourseAuthor, IsCourseTeacher
from course_app.serializers import (CourseAddTeachersAndStudentsSerializer,
                                    CourseCreateSerializer,
                                    CourseDetailsSerializer,
                                    CourseShortDetailsSerializer,
                                    CourseUpdateFullSerializer)
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from payments_app.choices import PaymentStatusChoices


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

    to_buy:
        Get all available to buy courses
    '''

    permission_classes = [permissions.IsAuthenticated]

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
            'to_buy': Course.objects.exclude(
                status=StatusChoices.CLOSED
            ).exclude(
                teachers=self.request.user.id
            ).exclude(
                students=self.request.user.id
            ).exclude(
                price=0
            ).exclude(
                payments__user=self.request.user.id,
                payments__payment__status=PaymentStatusChoices.SUCCEEDED
            ),
            'purchased': Course.objects.filter(
                status=StatusChoices.OPEN,
                payments__user=self.request.user.id,
                payments__payment__status=PaymentStatusChoices.SUCCEEDED
            ),
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
            'to_buy': CourseShortDetailsSerializer,
            'purchased': CourseShortDetailsSerializer,
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
            'to_buy': [],
            'purchased': [],
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

    @action(methods=['GET'], detail=False)
    def to_buy(self, request):
        '''Get a list of available to buy courses'''
        queryset = self.get_queryset()
        serializer = self.get_serializer_class()(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=False)
    def purchased(self, request):
        '''Get a list of all purchased courses'''
        queryset = self.get_queryset()
        serializer = self.get_serializer_class()(queryset, many=True)
        return Response(serializer.data)
