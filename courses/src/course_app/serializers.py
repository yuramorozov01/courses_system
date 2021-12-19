from course_app.models import Course
from django.contrib.auth import get_user_model
from rest_framework import serializers


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


class CourseUpdateFullSerializer(serializers.ModelSerializer):
    '''Serializer for updating a specified course.
    With this serializer course can be updated only by an author.
    '''

    author = CustomUserSerializer(read_only=True)
    status = serializers.CharField(source='get_status_display')

    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ['author',  'created_at']

    def validate_teachers(self, value):
        if self.instance is not None:
            if self.instance.author not in value:
                raise serializers.ValidationError('Author of course has to be a teacher of this course')
        return value


class CourseAddTeachersAndStudentsSerializer(serializers.ModelSerializer):
    '''Serializer for addition teachers and students to a course.
    Only teachers can add teachers and students to the course.
    '''

    author = CustomUserSerializer(read_only=True)
    status = serializers.CharField(read_only=True, source='get_status_display')

    class Meta:
        model = Course
        fields = '__all__'
        read_only_fields = ['title', 'created_at', 'starts_at', 'ends_at', 'author', 'status']

    def validate_teachers(self, value):
        if self.instance is not None:
            if self.instance.author not in value:
                raise serializers.ValidationError('Author of course has to be a teacher of this course')
        return value
