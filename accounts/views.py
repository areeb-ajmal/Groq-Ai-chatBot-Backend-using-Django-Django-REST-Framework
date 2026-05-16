from django.shortcuts import render
from rest_framework.views import APIView
from accounts.serializers import SignupSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny 
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework_simplejwt.views import TokenRefreshView
from accounts.tasks import send_welcome_email

# Create your views here.

class Signup_view(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            refresh = RefreshToken.for_user(user)

            send_welcome_email.delay(user_email=user.email, username=user.username)

            return Response(
                {
                'user' : serializer.data,
                'access' : str(refresh.access_token),
                'refresh' : str(refresh),
            }, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoginView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(username=email, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                "access" : str(refresh.access_token),
                "refresh" : str(refresh),
            })
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'error' : 'invalid credidentials or user not exists'} , status=status.HTTP_400_BAD_REQUEST)
    

    




