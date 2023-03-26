from rest_framework import serializers
from .models import Employee

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ('name', 'age', 'created_at', 'updated_at')

# upfile 
class FileUploadSerializer(serializers.Serializer):
    # upload 1 file 
    # file = serializers.FileField() 

    # upload nhiều file 
    files = serializers.ListField(
        child=serializers.FileField(),
        allow_empty=False,
        max_length=10 # tối đa 10 ảnh 
    )
# upfile 
