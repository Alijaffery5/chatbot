from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Chat

class UserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ['id', 'username', 'email', 'password']

class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ('id', 'user', 'content', 'start_time', 'end_time', 'session_id')

    def to_representation(self, instance):
        """Modify the keys in the response."""
        representation = super().to_representation(instance)
        # Change the keys in the representation dictionary
        return {
            'chat_id': representation['id'],  # Renaming 'id' to 'chat_id'
            'user_id': representation['user'],  # Renaming 'user' to 'user_id'
            'conversation': representation['content'],  # Renaming 'content' to 'chat_content'
            'start_time': representation['start_time'],
            'end_time': representation['end_time'],
            'session_identifier': representation['session_id']  # Renaming 'session_id' to 'session_identifier'
        }
