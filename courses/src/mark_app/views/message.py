from django.db.models import Q
from mark_app.models import Mark, Message
from mark_app.serializers import (MessageCreateSerializer,
                                  MessageDetailsSerializer,
                                  MessageShortDetailsSerializer,
                                  MessageUpdateSerializer)
from rest_framework import permissions, serializers, viewsets


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
                Q(mark__task__author=self.request.user.id)
            ),
            'list': Message.objects.filter(
                Q(mark__task__task_statement__lecture__course__teachers=self.request.user.id) |
                Q(mark__task__author=self.request.user.id)
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
            parent = Message.objects.filter(mark=mark).get(pk=self.request.data.get('parent'))
            serializer.save(author=self.request.user, mark=mark, parent=parent)
        except Mark.DoesNotExist:
            raise serializers.ValidationError('You can add messages only in teaching courses or in own tasks')
        except Message.DoesNotExist:
            raise serializers.ValidationError('Child message must be in the same mark as parent message!')
