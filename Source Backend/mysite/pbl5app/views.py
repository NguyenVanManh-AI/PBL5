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




from django.http import JsonResponse
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from .models import Attendance

def attendance_count(request):
    maxUser = User.objects.filter(role='user').count()
    # Tìm ngày đầu tiên của tuần (thứ 2)
    today = timezone.now().date()
    start_of_week = today - timedelta(days=today.weekday())

    # Tạo một danh sách để lưu số người điểm danh từ thứ 2 đến chủ nhật
    attendance_count = []

    # Lặp qua từng ngày trong tuần từ thứ 2 đến chủ nhật
    for i in range(7):
        # Tính toán ngày của từng ngày trong tuần
        date = start_of_week + timedelta(days=i)

        # Lấy số người điểm danh cho ngày hiện tại
        if (datetime.date(2023, 5, 10) <= date) and (date <= datetime.datetime.now().date()):
            count = Attendance.objects.filter(date_time__date=date).values('id_user').annotate(count=Count('id_user')).count()
        else:
            count = maxUser
        # Thêm số người điểm danh vào danh sách
        attendance_count.append(count)

    
    for i in range(7):
        attendance_count[i]= maxUser - attendance_count[i]
    # Trả về kết quả dưới dạng JSON
    return JsonResponse(attendance_count, safe=False)



from django.db.models import Count
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Attendance

import calendar

@csrf_exempt
def attendance_count_by_month(request):
    
    year = datetime.datetime.now().year
    maxUser = User.objects.filter(role='user').count()
    attendance_count = []

    for month in range(1, 13):
        # Lấy số ngày trong tháng
        num_days = calendar.monthrange(year, month)[1]

        # Lặp qua từng ngày trong tháng
        sum = 0
        for day in range(1, num_days + 1):
            date = datetime.date(year, month, day)
            
            if (datetime.date(2023, 5, 10) <= date) and (date <= datetime.datetime.now().date()):
                count = Attendance.objects.filter(date_time__date=date).values('id_user').annotate(count=Count('id_user')).count()
            else:
                count = maxUser
            sum += count
        attendance_count.append(maxUser*num_days - sum)

    # Trả về dữ liệu dưới dạng JSON
    return JsonResponse(attendance_count, safe=False)


from datetime import date, time
def attendance_year(request):
    maxUser = User.objects.filter(role='user').count()
    year = datetime.datetime.now().year
    
    dung_gio = 0
    vang_mat = 0
    tre_gio = 0

    for month in range(1, 13):
        num_days = calendar.monthrange(year, month)[1]
        for day in range(1, num_days+1):
            
            today = datetime.date(year, month, day)
            start_time = datetime.datetime.combine(today, time(hour=1)) #1 am UTC = 8 gio sang Viet Nam (1+7=8) 


            if (datetime.date(2023, 5, 10) <= today) and (today <= datetime.datetime.now().date()):   
           
                on_time_count = Attendance.objects.filter(date_time__date=today, date_time__lt=start_time).values('id_user').annotate(count=Count('id_user')).count()
                late_count = Attendance.objects.filter(date_time__date=today, date_time__gte=start_time).values('id_user').annotate(count=Count('id_user')).count()
                absent_count = maxUser - (on_time_count + late_count)
            else:
                on_time_count = 0
                late_count = 0
                absent_count = 0
                

            dung_gio += on_time_count
            vang_mat += absent_count
            tre_gio += late_count

    
    data = {
        'dung_gio': dung_gio,
        'vang_mat': vang_mat,
        'tre_gio': tre_gio,
    }
    return JsonResponse(data)

def attendance_month(request):
    maxUser = User.objects.filter(role='user').count()
        
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    num_days = calendar.monthrange(year, month)[1]

    dung_gio = 0
    vang_mat = 0
    tre_gio = 0
    for day in range(1, num_days+1):
        today = datetime.date(year, month, day)
        start_time = datetime.datetime.combine(today, time(hour=1)) #1 am UTC = 8 gio sang Viet Nam (1+7=8) 

        if (datetime.date(2023, 5, 10) <= today) and (today <= datetime.datetime.now().date()):   
            on_time_count = Attendance.objects.filter(date_time__date=today, date_time__lt=start_time).values('id_user').annotate(count=Count('id_user')).count()
            late_count = Attendance.objects.filter(date_time__date=today, date_time__gte=start_time).values('id_user').annotate(count=Count('id_user')).count()
            absent_count = maxUser - (on_time_count + late_count)
        else:
            on_time_count = 0
            late_count = 0
            absent_count = 0

        dung_gio += on_time_count
        vang_mat += absent_count
        tre_gio += late_count

    
    data = {
        'dung_gio': dung_gio,
        'vang_mat': vang_mat,
        'tre_gio': tre_gio,
    }
    return JsonResponse(data)

def attendance_day(request):
    today = date.today()

    start_time = datetime.datetime.combine(today, time(hour=1)) #1 am UTC = 8 gio sang Viet Nam (1+7=8) 
   
    on_time_count = Attendance.objects.filter(date_time__date=today, date_time__lt=start_time).values('id_user').annotate(count=Count('id_user')).count()
    late_count = Attendance.objects.filter(date_time__date=today, date_time__gte=start_time).values('id_user').annotate(count=Count('id_user')).count()
    maxUser = User.objects.filter(role='user').count()
    absent_count = maxUser - (on_time_count + late_count)
    
    data = {
        'dung_gio': on_time_count,
        'vang_mat': absent_count,
        'tre_gio': late_count,
    }
    return JsonResponse(data)

def num_user(request):
    maxUser = User.objects.filter(role='user').count()
    return JsonResponse({'so_nhan_vien': str(maxUser)})

