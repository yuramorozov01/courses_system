from rest_framework import serializers

from base_app.serializers import CustomUserSerializer
from task_app.models import TaskFile


class TaskFileCreateSerializer(serializers.ModelSerializer):
    '''Serializer for creating task files'''

    author = CustomUserSerializer(read_only=True)

    class Meta:
        model = TaskFile
        fields = '__all__'
        read_only_fields = ['author', 'task']


class TaskFileDetailsSerializer(serializers.ModelSerializer):
    '''Serializer for a specified task file
    This serializer provides detailed information about task file.'''

    file = serializers.FileField(read_only=True, allow_empty_file=True)
    author = CustomUserSerializer(read_only=True)

    class Meta:
        model = TaskFile
        exclude = ['task']
        read_only_fields = ['file', 'author']


class TaskFileUpdateSerializer(serializers.ModelSerializer):
    '''Serializer for updating a specified task file.
    With this serializer task file can be updated only by a task file author.
    '''

    file = serializers.FileField(allow_empty_file=True)
    author = CustomUserSerializer(read_only=True)

    class Meta:
        model = TaskFile
        fields = '__all__'
        read_only_fields = ['task', 'author']
