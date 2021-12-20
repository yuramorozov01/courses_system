from django.db.models import Q
from course_app.models import Course
from lecture_app.models import Lecture, LectureFile
from lecture_app.serializers import (LectureCreateSerializer,
                                     LectureDetailsSerializer,
                                     LectureFileCreateSerializer,
                                     LectureFileDetailsSerializer,
                                     LectureFileUpdateSerializer,
                                     LectureShortDetailsSerializer,
                                     LectureUpdateSerializer)
from rest_framework import permissions, serializers, viewsets


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

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        querysets_dict = {
            'create': Lecture.objects.filter(course__teachers=self.request.user.id),
            'destroy': Lecture.objects.filter(course__teachers=self.request.user.id),
            'retrieve': Lecture.objects.filter(
                Q(course__teachers=self.request.user.id) | Q(course__students=self.request.user.id)
            ),
            'list': Lecture.objects.filter(
                Q(course__teachers=self.request.user.id) | Q(course__students=self.request.user.id)
            ).filter(course=self.request.data.get('course')),
            'update': Lecture.objects.filter(course__teachers=self.request.user.id),
            'partial_update': Lecture.objects.filter(course__teachers=self.request.user.id),
        }
        queryset = querysets_dict.get(self.action)
        return queryset

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

    def perform_create(self, serializer):
        queryset = self.get_queryset()
        try:
            Course.objects\
                .filter(teachers=self.request.user.id)\
                .get(pk=self.request.data.get('course'))
            serializer.save(author=self.request.user)
        except Course.DoesNotExist:
            raise serializers.ValidationError('You can add lectures only in teaching courses')


class LectureFileViewSet(viewsets.ModelViewSet):
    '''
    create:
        Create a new lecture file.

    destroy:
        Delete a lecture file.
        Only a teacher of course can delete lecture file.

    retrieve:
        Get the specified lecture file.

    list:
        Get a list of all course lecture files.

    update:
        Update a lecture file.
        Only a teacher of course can update lecture file.

    partial_update:
        Update a lecture file.
        Only a teacher of course can update lecture file.
    '''

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        querysets_dict = {
            'create': LectureFile.objects.filter(lecture__course__teachers=self.request.user.id),
            'destroy': LectureFile.objects.filter(lecture__course__teachers=self.request.user.id),
            'retrieve': LectureFile.objects.filter(
                Q(lecture__course__teachers=self.request.user.id) | Q(lecture__course__students=self.request.user.id)
            ),
            'list': LectureFile.objects.filter(
                Q(lecture__course__teachers=self.request.user.id) | Q(lecture__course__students=self.request.user.id)
            ).filter(lecture=self.request.data.get('lecture')),
            'update': LectureFile.objects.filter(lecture__course__teachers=self.request.user.id),
            'partial_update': LectureFile.objects.filter(lecture__course__teachers=self.request.user.id),
        }
        queryset = querysets_dict.get(self.action)
        return queryset

    def get_serializer_class(self):
        serializers_dict = {
            'create': LectureFileCreateSerializer,
            'retrieve': LectureFileDetailsSerializer,
            'list': LectureFileDetailsSerializer,
            'update': LectureFileUpdateSerializer,
            'partial_update': LectureFileUpdateSerializer,
        }
        serializer_class = serializers_dict.get(self.action)
        return serializer_class

    def perform_create(self, serializer):
        queryset = self.get_queryset()
        try:
            Lecture.objects\
                .filter(course__teachers=self.request.user.id)\
                .get(pk=self.request.data.get('lecture'))
            serializer.save(author=self.request.user)
        except Lecture.DoesNotExist:
            raise serializers.ValidationError('You can add lecture files only in teaching courses')
