from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Employee
from .serializers import EmployeeSerializer

@api_view(['GET', 'DELETE', 'PUT'])
def get_delete_update_employee(request, pk):
    try:
        employee = Employee.objects.get(pk=pk)
    except Employee.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # get details of a single employee
    if request.method == 'GET':
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data)
    # delete a single employee
    elif request.method == 'DELETE':
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    # update details of a single employee
    elif request.method == 'PUT':
        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
def get_post_employee(request):
    # get all employee
    if request.method == 'GET':
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)
    # insert a new record for a employee
    elif request.method == 'POST':
        data = {
            'name': request.data.get('name'),
            'age': int(request.data.get('age'))
        }
        serializer = EmployeeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# up file
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse

# cũ 
# def upload(request):
#     if request.method == 'POST' and request.FILES['file']:
#         # Lưu file vào server
#         file = request.FILES['file']
#         fs = FileSystemStorage()
#         filename = fs.save(file.name, file)

#         # Trả về thông tin về file đã lưu
#         return JsonResponse({'filename': filename})
#     else:
#         return JsonResponse({'error': 'Invalid request'})
    
# upload 1 file  
# upfile  

from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import FileUploadSerializer

# class FileUploadView(APIView):
#     def post(self, request):
#         serializer = FileUploadSerializer(data=request.data)
#         if serializer.is_valid():
#             file = serializer.validated_data['file']
#             # Xử lý file tại đây
#             fs = FileSystemStorage()
#             filename = fs.save(file.name, file)
#             return JsonResponse({'filename': filename})
#         else:
#             return Response(serializer.errors, status=400)
# upfile 
# upload 1 file  

# upload nhiều file 
import os
import shutil
import json 
from rest_framework.parsers import MultiPartParser

from unidecode import unidecode # xóa dấu trong python 
from .models import Images

import random
import string
# trong python có một cái rất hay , nghĩa là nếu như upload cùng tên file đã có thì nó tự cộng thêm một chuỗi random để khỏi trùng
# vấn đề ở đây là ta phải lấy tên để lưu vào db => xử lý mệt vì 
# cách tốt nhất là chủ động cho nó không thể trùng nhau bằng cách mỗi lần tạo file mới là cộng thêm chuỗi random 10 kí tự 

def handle_uploaded_file(file,user_id,user_fullname):
    fs = FileSystemStorage()
    user_fullname = unidecode(user_fullname).replace(" ", "-")
    # file_name = user_id+'-'+user_fullname+'-'+file.name
    randomstring = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    file_name = user_id + '-' + user_fullname + '-' + randomstring + '-' + file.name 
    fs.save(file_name, file)
    # path = '/avatar/'
    # if not os.path.exists(path):
    #     os.makedirs(path)
    # with open(os.path.join(path, file.name), 'wb+') as destination:
    #     for chunk in file.chunks():
    #         destination.write(chunk)

    # Lưu thông tin file vào bảng Images
    image = Images()
    image.id_user = user_id
    image.image_path = '/avatar/' + file_name
    image.save()

class FileUploadView(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request, format=None):
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            user_data = json.loads(request.data['user']) # dưới client là chuyển object thành string 
            # lên đây chuyển string về lại json 
            user_id = user_data.get('id')
            user_fullname = user_data.get('fullname')
            for file in serializer.validated_data['files']:
                handle_uploaded_file(file,user_id,user_fullname)
            return Response({'status': 'OK'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# upload nhiều file 


# get images of user 
def get_images(request):
    id_user = request.GET.get('id_user')
    images = Images.objects.filter(id_user=id_user)
    data = [{'id': img.id, 'id_user': img.id_user, 'image_path': img.image_path} for img in images]
    return JsonResponse({'data': data})


# update images 
def update_images(request):
    id_removeimages = request.GET.get('id_removeimages')
    id_imgRemoves = id_removeimages.split(',')
    try:
        for id_img in id_imgRemoves:
            # lấy ra ảnh có id đó 
            image = Images.objects.get(id=id_img)
    
            # xóa ảnh 
            image_path = image.image_path # '/avatar/gAo23GXKEKDGaWiQrZyT-Nguyen-Van-Manh-VAK2JZQETN-4k.jpg'
            image_path = image_path[1:] # nhưng 'avatar/gAo23GXKEKDGaWiQrZyT-Nguyen-Van-Manh-VAK2JZQETN-4k.jpg' mới được 
            if os.path.exists(image_path):  # kiểm tra xem ảnh có tồn tại không
                os.remove(image_path)  # xóa ảnh
    
            # Xóa dữ liệu trong db 
            image.delete()

        # Trả về True nếu xóa thành công
        return JsonResponse({'status': 'OK'})
    except:
        # Trả về False nếu xóa không thành công
        return JsonResponse({'status': 'False'})


# def all_images(): => như thế này sẽ lỗi 
def all_images(request):
    images = Images.objects.filter()
    data = [{'id': img.id, 'id_user': img.id_user, 'image_path': img.image_path} for img in images]
    return JsonResponse({'data': data})

# removeimages = request.GET.get('removeimages')
# data = {
#     'name': request.data.get('name'),
#     'age': int(request.data.get('age'))
# }
# => ta chú ý là get và GET là khác nhau , GET là phương thức , get là lấy 