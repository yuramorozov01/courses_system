from rest_framework import serializers

from base_app.serializers import CustomUserSerializer
from lecture_app.models import LectureFile


class LectureFileCreateSerializer(serializers.ModelSerializer):
    '''Serializer for creating lecture files'''

    author = CustomUserSerializer(read_only=True)

    class Meta:
        model = LectureFile
        fields = '__all__'
        read_only_fields = ['author', 'lecture']


class LectureFileDetailsSerializer(serializers.ModelSerializer):
    '''Serializer for a specified lecture file
    This serializer provides detailed information about lecture file.'''

    file = serializers.FileField(read_only=True, allow_empty_file=True)
    author = CustomUserSerializer(read_only=True)

    class Meta:
        model = LectureFile
        exclude = ['lecture']
        read_only_fields = ['file', 'author']


class LectureFileUpdateSerializer(serializers.ModelSerializer):
    '''Serializer for updating a specified lecture file.
    With this serializer lecture file can be updated only by a course teacher.
    '''

    file = serializers.FileField(allow_empty_file=True)
    author = CustomUserSerializer(read_only=True)

    class Meta:
        model = LectureFile
        fields = '__all__'
        read_only_fields = ['lecture', 'author']
