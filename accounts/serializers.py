from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def create(self, validate_data):
        user = User.objects.create_user(
            email = validate_data['email'],
            username = validate_data['username'],
            password = validate_data['password']        
        )
        return user
    


