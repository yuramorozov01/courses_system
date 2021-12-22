from django.db.models import Q
from mark_app.models import Mark, Message
from mark_app.serializers import (MarkCreateSerializer, MarkDetailsSerializer,
                                  MarkShortDetailsSerializer,
                                  MarkUpdateSerializer,
                                  MessageCreateSerializer,
                                  MessageDetailsSerializer,
                                  MessageShortDetailsSerializer,
                                  MessageUpdateSerializer)
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


class MessageViewSet(viewsets.ModelViewSet):
    '''
    create:
        Create a new message.

    destroy:
        Delete a message.
        Only an author of message can delete message.

    retrieve:
        Get the specified message.

    list:
        Get a list of messages.

    update:
        Update a message.
        Only an author of message can update message.

    partial_update:
        Update a message.
        Only an author of message can update message.
    '''

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        querysets_dict = {
            'create': Message.objects.filter(
                Q(mark__task__task_statement__lecture__course__teachers=self.request.user.id) |
                Q(mark__task__author=self.request.user.id)
            ),
            'destroy': Message.objects.filter(author=self.request.user.id),
            'retrieve': Message.objects.filter(
                Q(mark__task__task_statement__lecture__course__teachers=self.request.user.id) |
                Q(author=self.request.user.id)
            ),
            'list': Message.objects.filter(
                Q(mark__task__task_statement__lecture__course__teachers=self.request.user.id) |
                Q(author=self.request.user.id)
            ).filter(mark=self.kwargs.get('mark_pk')),
            'update': Message.objects.filter(author=self.request.user.id),
            'partial_update': Message.objects.filter(author=self.request.user.id),
        }
        queryset = querysets_dict.get(self.action)
        return queryset

    def get_serializer_class(self):
        serializers_dict = {
            'create': MessageCreateSerializer,
            'retrieve': MessageDetailsSerializer,
            'list': MessageShortDetailsSerializer,
            'update': MessageUpdateSerializer,
            'partial_update': MessageUpdateSerializer,
        }
        serializer_class = serializers_dict.get(self.action)
        return serializer_class

    def perform_create(self, serializer):
        try:
            mark = Mark.objects\
                .filter(
                    Q(task__task_statement__lecture__course__teachers=self.request.user.id) |
                    Q(task__author=self.request.user.id)
                ).get(pk=self.kwargs.get('mark_pk'))
            serializer.save(author=self.request.user, mark=mark)
        except Task.DoesNotExist:
            raise serializers.ValidationError('You can add messages only in teaching courses or ')
