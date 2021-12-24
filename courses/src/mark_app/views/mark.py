from django.db.models import Q
from mark_app.models import Mark
from mark_app.serializers import (MarkCreateSerializer,
                                  MarkDetailsSerializer,
                                  MarkShortDetailsSerializer,
                                  MarkUpdateSerializer)
from rest_framework import permissions, serializers, viewsets
from task_app.models import Task


class MarkViewSet(viewsets.ModelViewSet):
    '''
    create:
        Create a new mark.

    destroy:
        Delete a mark.
        Only a teacher of course can delete mark.

    retrieve:
        Get the specified mark.

    list:
        Get a list of marks.

    update:
        Update a mark.
        Only a teacher of course can update mark.

    partial_update:
        Update a mark.
        Only a teacher of course can update mark.
    '''

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        querysets_dict = {
            'create': Mark.objects.filter(task__task_statement__lecture__course__teachers=self.request.user.id),
            'destroy': Mark.objects.filter(task__task_statement__lecture__course__teachers=self.request.user.id),
            'retrieve': Mark.objects.filter(
                Q(task__task_statement__lecture__course__teachers=self.request.user.id) |
                Q(task__author=self.request.user.id)
            ),
            'list': Mark.objects.filter(
                Q(task__task_statement__lecture__course__teachers=self.request.user.id) |
                Q(task__author=self.request.user.id)
            ).filter(task=self.kwargs.get('task_pk')),
            'update': Mark.objects.filter(task__task_statement__lecture__course__teachers=self.request.user.id),
            'partial_update': Mark.objects.filter(task__task_statement__lecture__course__teachers=self.request.user.id),
        }
        queryset = querysets_dict.get(self.action)
        return queryset

    def get_serializer_class(self):
        serializers_dict = {
            'create': MarkCreateSerializer,
            'retrieve': MarkDetailsSerializer,
            'list': MarkShortDetailsSerializer,
            'update': MarkUpdateSerializer,
            'partial_update': MarkUpdateSerializer,
        }
        serializer_class = serializers_dict.get(self.action)
        return serializer_class

    def perform_create(self, serializer):
        try:
            task = Task.objects\
                .filter(task_statement__lecture__course__teachers=self.request.user.id)\
                .get(pk=self.kwargs.get('task_pk'))
            serializer.save(author=self.request.user, task=task)
        except Task.DoesNotExist:
            raise serializers.ValidationError('You can add marks only in teaching courses')