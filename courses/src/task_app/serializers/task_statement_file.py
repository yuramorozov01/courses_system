from rest_framework import serializers

from base_app.serializers import CustomUserSerializer
from task_app.models import TaskStatementFile


class TaskStatementFileCreateSerializer(serializers.ModelSerializer):
    '''Serializer for creating task statement files'''

    author = CustomUserSerializer(read_only=True)

    class Meta:
        model = TaskStatementFile
        fields = '__all__'
        read_only_fields = ['author', 'task_statement']


class TaskStatementFileDetailsSerializer(serializers.ModelSerializer):
    '''Serializer for a specified task statement file
    This serializer provides detailed information about task statement file.'''

    file = serializers.FileField(read_only=True, allow_empty_file=True)
    author = CustomUserSerializer(read_only=True)

    class Meta:
        model = TaskStatementFile
        exclude = ['task_statement']
        read_only_fields = ['file', 'author']


class TaskStatementFileUpdateSerializer(serializers.ModelSerializer):
    '''Serializer for updating a specified task statement file.
    With this serializer task statement file can be updated only by a course teacher.
    '''

    file = serializers.FileField(allow_empty_file=True)
    author = CustomUserSerializer(read_only=True)

    class Meta:
        model = TaskStatementFile
        fields = '__all__'
        read_only_fields = ['task_statement', 'author']
