from django.shortcuts import render
from groq.resources import ChatWithRawResponse
from rest_framework.views import APIView
from .groq_client import get_groq_response
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Conversation, Message
from rest_framework import viewsets
from .serializers import MessageSerializer, ConversationSerializer
from rest_framework.decorators import action
from .throttles import AiChatThrottle
from django.core.cache import cache
from django.utils import timezone


# Create your views here.

class ChatCreate(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_message = request.data.get('message')
        conversation_id = request.data.get('conversation_id')

        if conversation_id:
            conversation = Conversation.objects.get(id=conversation_id, user=request.user)
        else:
            conversation = Conversation.objects.create(
                user=request.user,
                title=user_message[:50]
            )

        past_messages = conversation.messages.all().order_by('created_at')
        history = [{
            "role" : msg.role, "content" : msg.content
        } for msg in past_messages]

        messages = [{
            "role" : "system", "content" : "You are a helpful assistant"
        },*history,
        {
            "role" : "user" , "content" : user_message
        }]

        try:
            reply = get_groq_response(messages)
            Message.objects.create(conversation=conversation, role="user", content=user_message)
            Message.objects.create(conversation=conversation, role="assistant", content=reply)
            return Response({"reply" : reply, "conversation_id" : conversation.id}, status=201)

        except Exception as e:
            return Response({"error" : str(e)}, status=500)


class ChatDetailView(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticated]
    serializer_class = ConversationSerializer
    throttle_classes = [AiChatThrottle]


    def get_queryset(self):
            return Conversation.objects.filter(user=self.request.user)

    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        conversation = self.get_object()
        messages = conversation.messages.all().order_by('created_at')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    def list(self, request):
        queryset = self.get_queryset()
        cache_key = f"user_id_{request.user}"
        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data)
        serializer = ConversationSerializer(queryset, many=True)
        cache.set(cache_key, serializer.data, timeout=60 * 5)
        return Response(serializer.data)


    @action(detail=True, methods=['post'])
    def chat(self, request, pk=None):
        conversation = self.get_object()
        user_message = request.data.get('message')
        cache_key = f"user_id_{request.user.id}_user_message_{user_message}"
        cached_data = cache.get(cache_key)

        if not user_message:
            return Response({"error" : "Message is required"}, status=400)

        if cached_data:
            return Response({"reply" : cached_data})

        past_messages = conversation.messages.all().order_by('created_at')
        history = [
            {
                "role" : msg.role, "content" : msg.content
            }
            for msg in past_messages
        ]
        messages = [
            {
                "role" : "system", "content" : "You are a helpful assistant"
            },*history,
            {
                "role" : "user", "content" : user_message
            }
        ]

        try:
            Message.objects.create(conversation=conversation, role="user", content= user_message)
            start = timezone.now()
            reply = get_groq_response(messages)
            end = timezone.now()
            response_time = (end - start).total_seconds()
            Message.objects.create(conversation=conversation, role="assistant", content=reply, response_time=response_time)
            cache.set(cache_key, reply, timeout=60*5)
            return Response({'reply' : reply}, status=200)

        except Exception as e:
            return Response({"error" : str(e)}, status=500)



































