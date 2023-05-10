from django.contrib import admin
# Register your models here.
from .models import User, Encode, Attendance
 
admin.site.register(User)
admin.site.register(Encode)
admin.site.register(Attendance)
