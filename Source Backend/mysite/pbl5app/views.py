from rest_framework import viewsets
from .models import User, Encode, Attendance
from .serializers import UserSerializer, UserPasswordUpdateSerializer, EncodeSerializer
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

class EncodeList(generics.ListAPIView):
    queryset = Encode.objects.all()
    serializer_class = EncodeSerializer


class UserList(generics.ListAPIView):
    queryset = User.objects.filter(role='user').order_by('-id')
    serializer_class = UserSerializer

    
class AdminList(generics.ListAPIView):
    queryset = User.objects.filter(role='admin').order_by('-id')
    serializer_class = UserSerializer

import os
from django.conf import settings

from .ListEncodeFromVideo import ListEncodeVideo
import cv2


class UserUpdateAPIView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
       
    

        update_encode= 0
        if 'url_video' in request.data:
            update_encode= 1
            if instance.url_video:
                # Xoa encode cu
                Encode.objects.filter(id_user=str(instance.id)).delete()
              
                # Xóa video cũ
            
                path = instance.url_video.path
                if os.path.isfile(os.path.join(settings.MEDIA_ROOT, path)):
                    os.remove(os.path.join(settings.MEDIA_ROOT, path))
                

            # Lưu video mới
            instance.url_video = request.data['url_video']
            

        serializer.save()   # NOTE: update_encode de sau dong nay thi path moi chinh xac

        if update_encode==1:
            
            # tao encode moi        
            path = instance.url_video.path
            cap = cv2.VideoCapture(path)
            list_encodes = ListEncodeVideo(cap)
            for vector in list_encodes:
                new_encode = Encode(encode_user=str(vector), id_user=instance.id)
                new_encode.save()   
                
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
        
# import csv
# def save_encode_face(encode):
#     # Hàng mới cần thêm vào
#     new_row = encode

#     # Mở file CSV trong chế độ "append"
#     with open("./face_rasp_recog.csv", 'a', newline='') as file:
#         writer = csv.writer(file)

#         # Ghi hàng mới vào cuối file
#         writer.writerow(new_row)

# import base64
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import numpy as np

# @csrf_exempt
# def receive_encode_face(request):
#     if request.method == 'POST':
#         # Lấy dữ liệu encodeFace_bytes từ request POST
        
#         encodeFace_str = request.POST.get('encodeFace', None)
    

#         # Kiểm tra xem dữ liệu encodeFace_bytes có tồn tại hay không
#         if encodeFace_str is None:
#             return JsonResponse({'error': 'encodeFace_str == None'})
#         # Giải mã đối tượng bytes thành mảng numpy
#         encodeFace = np.fromstring(encodeFace_str[1:-1], sep=' ')
        
#         save_encode_face(encodeFace)
#             # Do something with encode_face , 'encode_face':encode_face
#         return JsonResponse({'status': 'success'})
#     else:
#         return JsonResponse({'status': 'error'})

import io
import face_recognition

def EncodeFrame(framS):
    return face_recognition.face_encodings(framS)


from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .tests import show

import numpy as np
import datetime
import re
@csrf_exempt
def receive_image(request):
    if request.method == 'POST':
        if 'image' in request.FILES:
            image_file = request.FILES['image']
            # Chuyển đổi image_file thành framS
            image_bytes = io.BytesIO(image_file.read())
            framS = face_recognition.load_image_file(image_bytes)
            cv2.imwrite("DEMOtruoc.jpg", framS)
            
            framS = cv2.resize(framS, (0, 0), None, fx=0.5, fy=0.5)
            framS = cv2.cvtColor(framS, cv2.COLOR_BGR2RGB)
            # cv2.imwrite("DEMO.jpg", framS)
            # Tính toán face encodings
            list_encode = EncodeFrame(framS)
            # lấy danh sách encode
            # nhận diện list_encode thành id tương ứng
            # thêm id vào danh sách điểm danh
            listEncodeRasp = []
            for val in list_encode: 
                listEncodeRasp.append(list(val))
            
            encodes = Encode.objects.all()
            list_userId = []
            list_userEncode = []
            for encode in encodes:
                data = encode.encode_user

                # Xóa ký tự "[" và "]" khỏi chuỗi dữ liệu
                data = data.replace("[", "").replace("]", "")

                # Chuyển chuỗi dữ liệu thành một danh sách các giá trị float
                data = [float(x) for x in data.split()]

                # Chuyển danh sách thành một numpy array
                np_array = np.array(data, dtype=np.float32)
                list_userEncode.append(np_array)  
                                
                list_userId.append(encode.id_user)
            
            list_userEncode = np.array(list_userEncode)

            if len(listEncodeRasp)  > 0:
                for encode_raps in listEncodeRasp:
                    user_encode_array = np.array(list_userEncode)
                    raps_encode_array = np.array(list(map(float, encode_raps)))
                    faceDis = face_recognition.face_distance(user_encode_array, raps_encode_array)
                    
                    matchIndex = np.argmin(faceDis)
                    if faceDis[matchIndex] < 0.60:
                        new_attendance = Attendance(id_user=list_userId[matchIndex],  date_time= datetime.datetime.now())
                        new_attendance.save()
            
            return JsonResponse({'message': 'Success', 'len':str(len(list_encode))})
        else:
            return JsonResponse({'message': 'No image found in request'}, status=400)
    else:
        return JsonResponse({'message': 'Invalid request method'}, status=405)


from rest_framework import generics
from .models import Attendance
from .serializers import AttendanceSerializer

class AttendanceByMonthAPIView(generics.ListAPIView):
    serializer_class = AttendanceSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']  # Lấy id người dùng từ URL
        month = self.kwargs['month']  # Lấy tháng từ URL
        year = self.kwargs['year']  # Lấy năm từ URL

        # Lấy điểm danh theo người dùng, tháng và năm
        queryset = Attendance.objects.filter(
            id_user=user_id,
            date_time__month=month,
            date_time__year=year
        ).order_by('date_time')

        # Chỉ lấy điểm danh sớm nhất của mỗi ngày
        attendance_dates = set()
        filtered_queryset = []
        for attendance in queryset:
            date = attendance.date_time.date()
            if date not in attendance_dates:
                attendance_dates.add(date)
                attendance.date_time = date
                filtered_queryset.append(attendance)

        return filtered_queryset
