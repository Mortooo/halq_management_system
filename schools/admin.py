from django.contrib import admin
from .models import School, UserProfile


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'tel', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name', 'address']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'school']
    list_filter = ['school']
    search_fields = ['user__username', 'user__first_name']
