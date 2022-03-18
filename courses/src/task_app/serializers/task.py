from base_app.serializers import CustomUserSerializer
from mark_app.serializers import MarkShortDetailsSerializer
from rest_framework import serializers
from task_app.models import Task
from task_app.serializers.task_file import TaskFileDetailsSerializer


class TaskCreateSerializer(serializers.ModelSerializer):
    '''Serializer for creating tasks'''

    author = CustomUserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['author', 'created_at', 'task_statement']


class TaskShortDetailsSerializer(serializers.ModelSerializer):
    '''Serializer for a specified task.
    This serializer provides short information about the task.
    '''

    author = CustomUserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'link', 'author', 'created_at']
        read_only_fields = ['link', 'author', 'created_at']


class TaskDetailsSerializer(serializers.ModelSerializer):
    '''Serializer for a specified task.
    This serializer provides detailed information about task.
    '''

    author = CustomUserSerializer(read_only=True)
    files = TaskFileDetailsSerializer(read_only=True, many=True)
    mark = MarkShortDetailsSerializer(read_only=True)

    class Meta:
        model = Task
        exclude = ['task_statement']
        read_only_fields = ['text', 'link', 'author', 'created_at']


class TaskUpdateSerializer(serializers.ModelSerializer):
    '''Serializer for updating a specified task.
    With this serializer task can be updated only by a task author.
    '''

    author = CustomUserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['task_statement', 'author',  'created_at']
