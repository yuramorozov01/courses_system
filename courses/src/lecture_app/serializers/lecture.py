from rest_framework import serializers

from base_app.serializers import CustomUserSerializer
from lecture_app.models import Lecture
from lecture_app.serializers.lecture_file import LectureFileDetailsSerializer
from task_app.serializers.task_statement import \
    TaskStatementShortDetailsSerializer


class LectureCreateSerializer(serializers.ModelSerializer):
    '''Serializer for creating lectures'''

    author = CustomUserSerializer(read_only=True)

    class Meta:
        model = Lecture
        fields = '__all__'
        read_only_fields = ['author', 'created_at', 'course']


class LectureDetailsSerializer(serializers.ModelSerializer):
    '''Serializer for a specified lecture
    This serializer provides detailed information about lecture.
    '''

    author = CustomUserSerializer(read_only=True)
    files = LectureFileDetailsSerializer(read_only=True, many=True)
    task_statements = TaskStatementShortDetailsSerializer(read_only=True, many=True)

    class Meta:
        model = Lecture
        exclude = ['course']
        read_only_fields = ['title', 'text', 'author', 'created_at']


class LectureShortDetailsSerializer(serializers.ModelSerializer):
    '''Serializer for a specified lecture
    TThis serializer provides short information about lecture.
    '''

    author = CustomUserSerializer(read_only=True)

    class Meta:
        model = Lecture
        fields = ['id', 'title', 'author', 'created_at']
        read_only_fields = ['title', 'author', 'created_at']


class LectureUpdateSerializer(serializers.ModelSerializer):
    '''Serializer for updating a specified lecture.
    With this serializer lecture can be updated only by a course teacher.
    '''

    author = CustomUserSerializer(read_only=True)

    class Meta:
        model = Lecture
        fields = '__all__'
        read_only_fields = ['course', 'author',  'created_at']
