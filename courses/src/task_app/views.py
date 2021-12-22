from django.db.models import Q
from lecture_app.models import Lecture
from rest_framework import permissions, serializers, viewsets
from task_app.models import Task, TaskFile, TaskStatement, TaskStatementFile
from task_app.serializers import (TaskCreateSerializer, TaskDetailsSerializer,
                                  TaskFileCreateSerializer,
                                  TaskFileDetailsSerializer,
                                  TaskFileUpdateSerializer,
                                  TaskShortDetailsSerializer,
                                  TaskStatementCreateSerializer,
                                  TaskStatementDetailsSerializer,
                                  TaskStatementFileCreateSerializer,
                                  TaskStatementFileDetailsSerializer,
                                  TaskStatementFileUpdateSerializer,
                                  TaskStatementShortDetailsSerializer,
                                  TaskStatementUpdateSerializer,
                                  TaskUpdateSerializer)


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
            ).filter(lecture=self.kwargs.get('lecture_pk')),
            'update': TaskStatement.objects.filter(lecture__course__teachers=self.request.user.id),
            'partial_update': TaskStatement.objects.filter(lecture__course__teachers=self.request.user.id),
        }
        queryset = querysets_dict.get(self.action)
        return queryset

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

    def perform_create(self, serializer):
        try:
            lecture = Lecture.objects\
                .filter(course__teachers=self.request.user.id)\
                .get(pk=self.kwargs.get('lecture_pk'))
            serializer.save(author=self.request.user, lecture=lecture)
        except Lecture.DoesNotExist:
            raise serializers.ValidationError('You can add task statements only in teaching courses')


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

    permission_classes = [permissions.IsAuthenticated]

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
            ).filter(task_statement=self.kwargs.get('task_statement_pk')),
            'update': TaskStatementFile.objects.filter(task_statement__lecture__course__teachers=self.request.user.id),
            'partial_update': TaskStatementFile.objects.filter(
                task_statement__lecture__course__teachers=self.request.user.id
            ),
        }
        queryset = querysets_dict.get(self.action)
        return queryset

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

    def perform_create(self, serializer):
        try:
            task_statement = TaskStatement.objects\
                .filter(lecture__course__teachers=self.request.user.id)\
                .get(pk=self.kwargs.get('task_statement_pk'))
            serializer.save(author=self.request.user, task_statement=task_statement)
        except TaskStatement.DoesNotExist:
            raise serializers.ValidationError('You can add task statement files only in teaching courses')


class TaskViewSet(viewsets.ModelViewSet):
    '''
    create:
        Create a new task.

    destroy:
        Delete a task.
        Only an author of task can delete task.

    retrieve:
        Get the specified task.
        Only a teacher of course and an author can view task.

    list:
        Get a list of all lecture tasks.
        Only a teacher of course and an author can view task.

    update:
        Update a task.
        Only an author of task can update the task.

    partial_update:
        Update a task.
        Only an author of task can update the task.
    '''

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        querysets_dict = {
            'create': Task.objects.filter(task_statement__lecture__course__students=self.request.user.id),
            'destroy': Task.objects.filter(author=self.request.user.id),
            'retrieve': Task.objects.filter(
                Q(task_statement__lecture__course__teachers=self.request.user.id) |
                Q(author=self.request.user.id)
            ),
            'list': Task.objects.filter(
                Q(task_statement__lecture__course__teachers=self.request.user.id) |
                Q(author=self.request.user.id)
            ).filter(task_statement=self.kwargs.get('task_statement_pk')),
            'update': Task.objects.filter(author=self.request.user.id),
            'partial_update': Task.objects.filter(author=self.request.user.id),
        }
        queryset = querysets_dict.get(self.action)
        return queryset

    def get_serializer_class(self):
        serializers_dict = {
            'create': TaskCreateSerializer,
            'retrieve': TaskDetailsSerializer,
            'list': TaskShortDetailsSerializer,
            'update': TaskUpdateSerializer,
            'partial_update': TaskUpdateSerializer,
        }
        serializer_class = serializers_dict.get(self.action)
        return serializer_class

    def perform_create(self, serializer):
        try:
            task_statement = TaskStatement.objects\
                .filter(lecture__course__students=self.request.user.id)\
                .get(pk=self.kwargs.get('task_statement_pk'))
            serializer.save(author=self.request.user, task_statement=task_statement)
        except TaskStatement.DoesNotExist:
            raise serializers.ValidationError('You can add tasks only in studying courses')


class TaskFileViewSet(viewsets.ModelViewSet):
    '''
    create:
        Create a new task file.

    destroy:
        Delete a task file.
        Only an author of task file can delete task file.

    retrieve:
        Get the specified task file.

    list:
        Get a list of all task files.

    update:
        Update a task file.
        Only an author of task file can update task file.

    partial_update:
        Update a task file.
        Only an author of task file can update task file.
    '''

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        querysets_dict = {
            'create': TaskFile.objects.filter(author=self.request.user.id),
            'destroy': TaskFile.objects.filter(author=self.request.user.id),
            'retrieve': TaskFile.objects.filter(
                Q(task__task_statement__lecture__course__teachers=self.request.user.id) |
                Q(author=self.request.user.id)
            ),
            'list': TaskFile.objects.filter(
                Q(task__task_statement__lecture__course__teachers=self.request.user.id) |
                Q(author=self.request.user.id)
            ).filter(task=self.kwargs.get('task_pk')),
            'update': TaskFile.objects.filter(author=self.request.user.id),
            'partial_update': TaskFile.objects.filter(author=self.request.user.id),
        }
        queryset = querysets_dict.get(self.action)
        return queryset

    def get_serializer_class(self):
        serializers_dict = {
            'create': TaskFileCreateSerializer,
            'retrieve': TaskFileDetailsSerializer,
            'list': TaskFileDetailsSerializer,
            'update': TaskFileUpdateSerializer,
            'partial_update': TaskFileUpdateSerializer,
        }
        serializer_class = serializers_dict.get(self.action)
        return serializer_class

    def perform_create(self, serializer):
        try:
            task = Task.objects\
                .filter(task_statement__lecture__course__students=self.request.user.id)\
                .get(pk=self.kwargs.get('task_pk'))
            serializer.save(author=self.request.user, task=task)
        except Task.DoesNotExist:
            raise serializers.ValidationError('You can add task files only in studying courses')
