from rest_framework import serializers
from .models import Message, Conversation

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['role', 'content', 'created_at']

class ConversationSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Conversation
        fields = ['id','user', 'title', 'created_at']
        extra_krargs = {
            'title' : {'required' : False, 'allow_blank' : True}
        }




