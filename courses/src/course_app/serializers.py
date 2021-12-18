from django.contrib.auth import get_user_model
from rest_framework import serializers
from course_app.models import Course


class CustomUserSerializer(serializers.ModelSerializer):
    '''Serializer for an user'''

    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'email']


class CourseCreateSerializer(serializers.ModelSerializer):
    '''Serializer for creating courses'''

    author = CustomUserSerializer(read_only=True)
    teachers = CustomUserSerializer(read_only=True, many=True)

    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ['author', 'teachers', 'students', 'status', 'created_at']


class CourseDetailsSerializer(serializers.ModelSerializer):
    '''Serializer for a specified course
    This serializer provides detailed information about course.
    '''

    author = CustomUserSerializer(read_only=True)
    teachers = CustomUserSerializer(read_only=True, many=True)
    students = CustomUserSerializer(read_only=True, many=True)
    status = serializers.CharField(source='get_status_display')

    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ['title', 'created_at', 'starts_at', 'ends_at', 'author', 'teachers', 'students', 'status']


class CourseShortDetailsSerializer(serializers.ModelSerializer):
    '''Serializer for a specified course
    This serializer provides short information about course.
    '''

    author = CustomUserSerializer(read_only=True)
    status = serializers.CharField(source='get_status_display')

    class Meta:
        model = Course
        exclude = ['created_at', 'students', 'teachers']
        read_only_fields = ['title', 'starts_at', 'ends_at', 'author', 'status']
