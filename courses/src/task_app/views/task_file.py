from django.db.models import Q
from rest_framework import permissions, serializers, viewsets
from task_app.models import Task, TaskFile
from task_app.serializers import (TaskFileCreateSerializer,
                                  TaskFileDetailsSerializer,
                                  TaskFileUpdateSerializer)


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
            ),
            'update': TaskFile.objects.filter(author=self.request.user.id),
            'partial_update': TaskFile.objects.filter(author=self.request.user.id),
        }
        queryset = querysets_dict.get(self.action)
        return queryset.filter(task=self.kwargs.get('task_pk')).distinct()

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
