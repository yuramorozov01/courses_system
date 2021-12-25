from django.db.models import Q
from lecture_app.models import Lecture
from rest_framework import permissions, serializers, viewsets
from task_app.models import TaskStatement
from task_app.serializers import (TaskStatementCreateSerializer,
                                  TaskStatementDetailsSerializer,
                                  TaskStatementShortDetailsSerializer,
                                  TaskStatementUpdateSerializer)
from course_app.permissions import IsCourseAuthor, IsCourseTeacher, IsCourseTeacherOrStudent


class TaskStatementViewSet(viewsets.ModelViewSet):
    '''
    create:
        Create a new task statement.

    destroy:
        Delete a task statement.
        Only a teacher of course can delete task statement.

    retrieve:
        Get the specified task statement.

    list:
        Get a list of all lecture task statements.

    update:
        Update a task statement.
        Only a teacher of course can update task statement.

    partial_update:
        Update a task statement.
        Only a teacher of course can update task statement.
    '''

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        querysets_dict = {
            'create': TaskStatement.objects.filter(lecture__course__teachers=self.request.user.id),
            'destroy': TaskStatement.objects.filter(lecture__course__teachers=self.request.user.id),
            'retrieve': TaskStatement.objects.filter(
                Q(lecture__course__teachers=self.request.user.id) | Q(lecture__course__students=self.request.user.id)
            ),
            'list': TaskStatement.objects.filter(
                Q(lecture__course__teachers=self.request.user.id) | Q(lecture__course__students=self.request.user.id)
            ),
            'update': TaskStatement.objects.filter(lecture__course__teachers=self.request.user.id),
            'partial_update': TaskStatement.objects.filter(lecture__course__teachers=self.request.user.id),
        }
        queryset = querysets_dict.get(self.action)
        return queryset.filter(lecture=self.kwargs.get('lecture_pk')).distinct()

    def get_serializer_class(self):
        serializers_dict = {
            'create': TaskStatementCreateSerializer,
            'retrieve': TaskStatementDetailsSerializer,
            'list': TaskStatementShortDetailsSerializer,
            'update': TaskStatementUpdateSerializer,
            'partial_update': TaskStatementUpdateSerializer,
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
            raise serializers.ValidationError('You can add task statements only in teaching courses')
