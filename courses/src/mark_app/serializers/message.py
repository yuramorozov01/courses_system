from base_app.serializers import CustomUserSerializer
from mark_app.models import Message
from rest_framework import serializers


class MessageCreateSerializer(serializers.ModelSerializer):
    '''Serializer for creating message'''

    author = CustomUserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = '__all__'
        read_only_fields = ['mark', 'author', 'parent', 'created_at']


class RecursiveMessageChildrenSerializer(serializers.Serializer):
    '''Serializer for recursive output children of message model'''

    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class FilterMessageListSerrializer(serializers.ListSerializer):
    '''Filter to output only parent messages'''

    def to_representation(self, data):
        data = data.filter(parent=None)
        return super().to_representation(data)


class MessageDetailsSerializer(serializers.ModelSerializer):
    '''Serializer for a message
    This serializer provides detailed information about message
    "children" field - related field to parent (get all message where current message is a parent message)
    '''

    author = CustomUserSerializer(read_only=True)
    children = RecursiveMessageChildrenSerializer(read_only=True, many=True)

    class Meta:
        model = Message
        exclude = ['mark']
        read_only_fields = ['text', 'author', 'parent', 'created_at']

        # Children messages output ...
        # ... with their parent messages at the same nesting level
        # So to prevent this, we have to filter messages to output ...
        # messages without parent messages - at the zero nesting level have to be ...
        # ... messages without parent messages
        list_serializer_class = FilterMessageListSerrializer


class MessageShortDetailsSerializer(serializers.ModelSerializer):
    '''Serializer for a message
    This serializer provides short information about the message.
    '''

    author = CustomUserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'author', 'created_at']
        read_only_fields = ['mark', 'text', 'parent', 'author', 'created_at']


class MessageUpdateSerializer(serializers.ModelSerializer):
    '''Serializer for updating message'''

    author = CustomUserSerializer(read_only=True)

    class Meta:
        model = Message
        exclude = ['mark']
        read_only_fields = ['parent', 'author', 'created_at']

    def validate(self, data):
        # Check that child is in the same mark as parent
        if data.get('parent') is not None:
            if data.get('parent').mark != data.get('mark'):
                raise serializers.ValidationError('Child message must be in the same mark as parent message!')
        return data
