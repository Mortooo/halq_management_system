from django.contrib import admin
from .models import StudAttendance,TeachAttendance

# Register your models here.
admin.site.register(StudAttendance)
admin.site.register(TeachAttendance)