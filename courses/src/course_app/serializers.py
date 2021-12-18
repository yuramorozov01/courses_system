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
