from .models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'role', 'password', 'fullname', 'url_video', 'phone', 'create_at', 'update_at']

