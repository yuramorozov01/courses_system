from course_app.models import Course
from django.db.models import Q
from lecture_app.models import Lecture
from lecture_app.serializers import (LectureCreateSerializer,
                                     LectureDetailsSerializer,
                                     LectureShortDetailsSerializer,
                                     LectureUpdateSerializer)
from rest_framework import permissions, serializers, viewsets
from course_app.permissions import IsCourseAuthor, IsCourseTeacher, IsCourseTeacherOrStudent


class LectureViewSet(viewsets.ModelViewSet):
    '''
    create:
        Create a new lecture.

    destroy:
        Delete a lecture.
        Only a teacher of course can delete lecture.

    retrieve:
        Get the specified lecture.

    list:
        Get a list of all course lectures.

    update:
        Update a lecture.
        Only a teacher of course can update lecture.

    partial_update:
        Update a lecture.
        Only a teacher of course can update lecture.
    '''

    def get_queryset(self):
        querysets_dict = {
            'create': Lecture.objects.filter(course__teachers=self.request.user.id),
            'destroy': Lecture.objects.filter(course__teachers=self.request.user.id),
            'retrieve': Lecture.objects.filter(
                Q(course__teachers=self.request.user.id) | Q(course__students=self.request.user.id)
            ),
            'list': Lecture.objects.filter(
                Q(course__teachers=self.request.user.id) | Q(course__students=self.request.user.id)
            ),
            'update': Lecture.objects.filter(course__teachers=self.request.user.id),
            'partial_update': Lecture.objects.filter(course__teachers=self.request.user.id),
        }
        queryset = querysets_dict.get(self.action)
        return queryset.filter(course=self.kwargs.get('course_pk')).distinct()

    def get_serializer_class(self):
        serializers_dict = {
            'create': LectureCreateSerializer,
            'retrieve': LectureDetailsSerializer,
            'list': LectureShortDetailsSerializer,
            'update': LectureUpdateSerializer,
            'partial_update': LectureUpdateSerializer,
        }
        serializer_class = serializers_dict.get(self.action)
        return serializer_class

    def get_permissions(self):
        base_permissions = [permissions.IsAuthenticated]
        permissions_dict = {
            'create': [IsCourseTeacher],
            'destroy': [IsCourseAuthor],
            'retrieve': [IsCourseTeacherOrStudent],
            'list': [IsCourseTeacherOrStudent],
            'update': [IsCourseAuthor],
            'partial_update': [IsCourseTeacher],
        }
        base_permissions += permissions_dict.get(self.action, [])
        return [permission() for permission in base_permissions]

    def perform_create(self, serializer):
        try:
            course = Course.objects\
                .filter(teachers=self.request.user.id)\
                .get(pk=self.kwargs.get('course_pk'))
            serializer.save(author=self.request.user, course=course)
        except Course.DoesNotExist:
            raise serializers.ValidationError('You can add lectures only in teaching courses')
