from django.db.models import Q
from rest_framework import permissions, serializers, viewsets
from task_app.models import Task, TaskStatement
from task_app.serializers import (TaskCreateSerializer, TaskDetailsSerializer,
                                  TaskShortDetailsSerializer,
                                  TaskUpdateSerializer)


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
