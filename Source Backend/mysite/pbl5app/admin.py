from django.contrib import admin
# Register your models here.
from .models import User, Encode
 
admin.site.register(User)
admin.site.register(Encode)

from .models import Attendance
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('id_user', 'date_time')  # Danh sách các trường muốn hiển thị
admin.site.register(Attendance, AttendanceAdmin)