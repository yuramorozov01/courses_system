from base_app.serializers import CustomUserSerializer
from mark_app.models import Mark
from rest_framework import serializers
from mark_app.serializers.message import MessageDetailsSerializer


class MarkCreateSerializer(serializers.ModelSerializer):
    '''Serializer for creating marks'''

    author = CustomUserSerializer(read_only=True)

    class Meta:
        model = Mark
        fields = '__all__'
        read_only_fields = ['author', 'updated_at', 'task']


class MarkDetailsSerializer(serializers.ModelSerializer):
    '''Serializer for a specified mark
    This serializer provides detailed information about the mark.
    '''

    author = CustomUserSerializer(read_only=True)
    messages = MessageDetailsSerializer(read_only=True, many=True)

    class Meta:
        model = Mark
        exclude = ['task']
        read_only_fields = ['mark_value', 'author', 'updated_at']


class MarkShortDetailsSerializer(serializers.ModelSerializer):
    '''Serializer for a specified mark
    This serializer provides short information about the mark.
    '''

    author = CustomUserSerializer(read_only=True)

    class Meta:
        model = Mark
        exclude = ['task']
        read_only_fields = ['mark_value', 'author', 'updated_at']


class MarkUpdateSerializer(serializers.ModelSerializer):
    '''Serializer for updating a specified mark.
    With this serializer mark can be updated only by a course teacher.
    '''

    author = CustomUserSerializer(read_only=True)

    class Meta:
        model = Mark
        fields = '__all__'
        read_only_fields = ['task', 'author',  'updated_at']
