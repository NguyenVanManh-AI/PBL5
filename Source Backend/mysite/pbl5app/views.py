from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer
# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

import hashlib

def hash_password(password):
    salt = "random string to make the hash more secure"
    salted_password = password + salt
    hashed_password = hashlib.sha256(salted_password.encode('utf-8')).hexdigest()
    return hashed_password

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'User does not exist'}, status=status.HTTP_401_UNAUTHORIZED)

        if hash_password(password) == user.password:
            serializer = UserSerializer(user)
            return Response(serializer.data)
        else:
            return Response({'error': user.password, 'errorx': hash_password(password)}, status=status.HTTP_401_UNAUTHORIZED)


from rest_framework import generics

class UserList(generics.ListAPIView):
    queryset = User.objects.filter(role='user').order_by('-id')
    serializer_class = UserSerializer

    
class AdminList(generics.ListAPIView):
    queryset = User.objects.filter(role='admin').order_by('-id')
    serializer_class = UserSerializer

import os
from django.conf import settings

class UserUpdateAPIView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        if 'url_video' in request.data:
            # Xóa video cũ
            if instance.url_video:
                path = instance.url_video.path
                if os.path.isfile(os.path.join(settings.MEDIA_ROOT, path)):
                    os.remove(os.path.join(settings.MEDIA_ROOT, path))
                    
            # Lưu video mới
            instance.url_video = request.data['url_video']


        serializer.save()
        return Response(serializer.data)