from base_app.serializers import CustomUserSerializer
from rest_framework import serializers
from task_app.models import Task, TaskFile, TaskStatement, TaskStatementFile


class TaskStatementCreateSerializer(serializers.ModelSerializer):
    '''Serializer for creating task statements'''

    author = CustomUserSerializer(read_only=True)

    class Meta:
        model = TaskStatement
        fields = '__all__'
        read_only_fields = ['author', 'created_at']


class TaskStatementFileDetailsSerializer(serializers.ModelSerializer):
    '''Serializer for a specified task statement file
    This serializer provides detailed information about task statement file.'''

    file = serializers.FileField(read_only=True, allow_empty_file=True)
    author = CustomUserSerializer(read_only=True)

    class Meta:
        model = TaskStatementFile
        exclude = ['task_statement']
        read_only_fields = ['file', 'author']


class TaskShortDetailsSerializer(serializers.ModelSerializer):
    '''Serializer for a specified task.
    This serializer provides short information about the task.
    '''

    author = CustomUserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = ['id', 'link', 'author', 'created_at']
        read_only_fields = ['link', 'author', 'created_at']


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


class TaskStatementFileCreateSerializer(serializers.ModelSerializer):
    '''Serializer for creating task statement files'''

    author = CustomUserSerializer(read_only=True)

    class Meta:
        model = TaskStatementFile
        fields = '__all__'
        read_only_fields = ['author']


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


class TaskCreateSerializer(serializers.ModelSerializer):
    '''Serializer for creating tasks'''

    author = CustomUserSerializer(read_only=True)

    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['author', 'created_at']


class TaskFileDetailsSerializer(serializers.ModelSerializer):
    '''Serializer for a specified task file
    This serializer provides detailed information about task file.'''

    file = serializers.FileField(read_only=True, allow_empty_file=True)
    author = CustomUserSerializer(read_only=True)

    class Meta:
        model = TaskFile
        exclude = ['task']
        read_only_fields = ['file', 'author']


class TaskDetailsSerializer(serializers.ModelSerializer):
    '''Serializer for a specified task.
    This serializer provides detailed information about task.
    '''

    author = CustomUserSerializer(read_only=True)
    files = TaskFileDetailsSerializer(read_only=True, many=True)

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


class TaskFileCreateSerializer(serializers.ModelSerializer):
    '''Serializer for creating task files'''

    author = CustomUserSerializer(read_only=True)

    class Meta:
        model = TaskFile
        fields = '__all__'
        read_only_fields = ['author']


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
