from .models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'role', 'password', 'fullname', 'url_video', 'phone', 'create_at', 'update_at']

class UserPasswordUpdateSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ('old_password', 'new_password')