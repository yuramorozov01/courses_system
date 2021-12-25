from course_app.permissions import (IsCourseTeacher,
                                    IsCourseTeacherOrStudent)
from django.db.models import Q
from rest_framework import permissions, serializers, viewsets
from task_app.models import TaskStatement, TaskStatementFile
from task_app.serializers import (TaskStatementFileCreateSerializer,
                                  TaskStatementFileDetailsSerializer,
                                  TaskStatementFileUpdateSerializer)


class TaskStatementFileViewSet(viewsets.ModelViewSet):
    '''
    create:
        Create a new task statement file.

    destroy:
        Delete a task statement file.
        Only a teacher of course can delete task statement file.

    retrieve:
        Get the specified task statement file.

    list:
        Get a list of all task statement files.

    update:
        Update a task statement file.
        Only a teacher of course can update task statement file.

    partial_update:
        Update a task statement file.
        Only a teacher of course can update task statement file.
    '''

    def get_queryset(self):
        querysets_dict = {
            'create': TaskStatementFile.objects.filter(task_statement__lecture__course__teachers=self.request.user.id),
            'destroy': TaskStatementFile.objects.filter(task_statement__lecture__course__teachers=self.request.user.id),
            'retrieve': TaskStatementFile.objects.filter(
                Q(task_statement__lecture__course__teachers=self.request.user.id) |
                Q(task_statement__lecture__course__students=self.request.user.id)
            ),
            'list': TaskStatementFile.objects.filter(
                Q(task_statement__lecture__course__teachers=self.request.user.id) |
                Q(task_statement__lecture__course__students=self.request.user.id)
            ),
            'update': TaskStatementFile.objects.filter(task_statement__lecture__course__teachers=self.request.user.id),
            'partial_update': TaskStatementFile.objects.filter(
                task_statement__lecture__course__teachers=self.request.user.id
            ),
        }
        queryset = querysets_dict.get(self.action)
        return queryset.filter(task_statement=self.kwargs.get('task_statement_pk')).distinct()

    def get_serializer_class(self):
        serializers_dict = {
            'create': TaskStatementFileCreateSerializer,
            'retrieve': TaskStatementFileDetailsSerializer,
            'list': TaskStatementFileDetailsSerializer,
            'update': TaskStatementFileUpdateSerializer,
            'partial_update': TaskStatementFileUpdateSerializer,
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
            task_statement = TaskStatement.objects\
                .filter(lecture__course__teachers=self.request.user.id)\
                .get(pk=self.kwargs.get('task_statement_pk'))
            serializer.save(author=self.request.user, task_statement=task_statement)
        except TaskStatement.DoesNotExist:
            raise serializers.ValidationError('You can add task statement files only in teaching courses')
