from course_app.permissions import (IsCourseTeacher,
                                    IsCourseTeacherOrStudent)
from django.db.models import Q
from lecture_app.models import Lecture, LectureFile
from lecture_app.serializers import (LectureFileCreateSerializer,
                                     LectureFileDetailsSerializer,
                                     LectureFileUpdateSerializer)
from rest_framework import permissions, serializers, viewsets


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
            ),
            'update': LectureFile.objects.filter(lecture__course__teachers=self.request.user.id),
            'partial_update': LectureFile.objects.filter(lecture__course__teachers=self.request.user.id),
        }
        queryset = querysets_dict.get(self.action)
        return queryset.filter(lecture=self.kwargs.get('lecture_pk')).distinct()

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

    def get_permissions(self):
        base_permissions = [permissions.IsAuthenticated]
        permissions_dict = {
            'create': [IsCourseTeacher],
            'destroy': [IsCourseTeacher],
            'retrieve': [IsCourseTeacherOrStudent],
            'list': [IsCourseTeacherOrStudent],
            'update': [IsCourseTeacher],
            'partial_update': [IsCourseTeacher],
        }
        base_permissions += permissions_dict.get(self.action, [])
        return [permission() for permission in base_permissions]

    def perform_create(self, serializer):
        try:
            lecture = Lecture.objects\
                .filter(course__teachers=self.request.user.id)\
                .get(pk=self.kwargs.get('lecture_pk'))
            serializer.save(author=self.request.user, lecture=lecture)
        except Lecture.DoesNotExist:
            raise serializers.ValidationError('You can add lecture files only in teaching courses')
