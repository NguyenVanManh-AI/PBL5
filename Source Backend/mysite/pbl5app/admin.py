from django.contrib import admin
# Register your models here.
from .models import User, ListEncode, Attendance
 
admin.site.register(User)
admin.site.register(ListEncode)
admin.site.register(Attendance)
