from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer, UserPasswordUpdateSerializer
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
import face_recognition

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
    

class UserPasswordUpdateAPIView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserPasswordUpdateSerializer
    #permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        old_password = hash_password(request.data.get('old_password'))
        new_password = hash_password(request.data.get('new_password'))
        if old_password == instance.password:
            instance.password = new_password
            instance.save(update_fields=['password'])
            # serializer = self.get_serializer(instance)
            return Response({'message': 'Password Changed'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Incorrect Old Password'}, status=status.HTTP_400_BAD_REQUEST)
        
import csv
def save_encode_face(encode):
    # Hàng mới cần thêm vào
    new_row = encode

    # Mở file CSV trong chế độ "append"
    with open("./face_rasp_recog.csv", 'a', newline='') as file:
        writer = csv.writer(file)

        # Ghi hàng mới vào cuối file
        writer.writerow(new_row)

import base64
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import numpy as np

@csrf_exempt
def receive_encode_face(request):
    if request.method == 'POST':
        # Lấy dữ liệu encodeFace_bytes từ request POST
        
        encodeFace_str = request.POST.get('encodeFace', None)
    

        # Kiểm tra xem dữ liệu encodeFace_bytes có tồn tại hay không
        if encodeFace_str is None:
            return JsonResponse({'error': 'encodeFace_str == None'})
        # Giải mã đối tượng bytes thành mảng numpy
        encodeFace = np.fromstring(encodeFace_str[1:-1], sep=' ')
        
        save_encode_face(encodeFace)
            # Do something with encode_face , 'encode_face':encode_face
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error'})

import io
import face_recognition

def Encode(framS):
    return face_recognition.face_encodings(framS)

@csrf_exempt
def receive_image(request):
    if request.method == 'POST':
        if 'image' in request.FILES:
            image_file = request.FILES['image']
            # Chuyển đổi image_file thành framS
            image_bytes = io.BytesIO(image_file.read())
            framS = face_recognition.load_image_file(image_bytes)
            # Tính toán face encodings
            list_encode = Encode(framS)
            # lấy danh sách encode
            # nhận diện list_encode thành id tương ứng
            # thêm id vào danh sách điểm danh

            return JsonResponse({'message': 'Success', 'list_encode': str(list_encode)})
        else:
            return JsonResponse({'message': 'No image found in request'}, status=400)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)
