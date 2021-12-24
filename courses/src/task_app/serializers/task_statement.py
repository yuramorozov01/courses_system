from base_app.serializers import CustomUserSerializer
from rest_framework import serializers
from task_app.models import TaskStatement
from task_app.serializers.task import TaskShortDetailsSerializer
from task_app.serializers.task_statement_file import \
    TaskStatementFileDetailsSerializer


class TaskStatementCreateSerializer(serializers.ModelSerializer):
    '''Serializer for creating task statements'''

    author = CustomUserSerializer(read_only=True)

    class Meta:
        model = TaskStatement
        fields = '__all__'
        read_only_fields = ['author', 'created_at', 'lecture']


class TaskStatementDetailsSerializer(serializers.ModelSerializer):
    '''Serializer for a specified task statement
    This serializer provides detailed information about task statement.
    '''

    author = CustomUserSerializer(read_only=True)
    files = TaskStatementFileDetailsSerializer(read_only=True, many=True)
    tasks = TaskShortDetailsSerializer(read_only=True, many=True)

    class Meta:
        model = TaskStatement
        exclude = ['lecture']
        read_only_fields = ['title', 'text', 'author', 'created_at']


class TaskStatementShortDetailsSerializer(serializers.ModelSerializer):
    '''Serializer for a specified task statement
    This serializer provides short information about task statement.
    '''

    author = CustomUserSerializer(read_only=True)

    class Meta:
        model = TaskStatement
        fields = ['id', 'title', 'author', 'created_at']
        read_only_fields = ['title', 'author', 'created_at']


class TaskStatementUpdateSerializer(serializers.ModelSerializer):
    '''Serializer for updating a specified task statement.
    With this serializer task statement can be updated only by a course teacher.
    '''

    author = CustomUserSerializer(read_only=True)

    class Meta:
        model = TaskStatement
        fields = '__all__'
        read_only_fields = ['lecture', 'author',  'created_at']
