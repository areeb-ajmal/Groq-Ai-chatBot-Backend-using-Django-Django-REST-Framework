from django.shortcuts import render
from rest_framework.views import APIView
from chat.models import Message
from rest_framework.permissions import IsAuthenticated
from django.db import connection
from rest_framework.response import Response
# Create your views here.


class MessageSummary(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        with connection.cursor() as cursor:
            cursor.execute(
                '''
                    SELECT COUNT(*) as total_messages
                    FROM chat_message as m
                    INNER JOIN chat_conversation as c
                    ON m.conversation_id = c.id
                    WHERE c.user_id = %s
                '''
                ,[request.user.id]
            )
            total_messages = cursor.fetchone()[0]

        with connection.cursor() as cursor:
            cursor.execute(
                '''
                    SELECT COUNT(DISTINCT c.user_id) as active_users
                    FROM chat_message as m 
                    INNER JOIN chat_conversation as c
                    ON m.conversation_id = c.id
                ''')
            active_users = cursor.fetchone()[0]
        return Response({"total_messages" : total_messages, "active_users" : active_users})
    
class MostActiveUsers(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        with connection.cursor() as cursor:
            cursor.execute(
                '''
                    SELECT COUNT(c.id) as conversation_count,
                    u.username as Users
                    FROM chat_conversation as c
                    JOIN accounts_customuser as u
                    ON c.user_id = u.id
                    GROUP BY u.id, u.username
                    ORDER BY conversation_count DESC
                    LIMIT 3;
                '''
            )
            rows = cursor.fetchall()

            user = [
                {'user' : row[1] , 'conversation_count' : row[0]}
                for row in rows
            ]

        return Response(user)
    







