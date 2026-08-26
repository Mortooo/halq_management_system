from django.db import models
from django.contrib.auth.models import User


class School(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='اسم المدرسة')
    address = models.CharField(max_length=200, blank=True, verbose_name='العنوان')
    tel = models.CharField(max_length=15, blank=True, verbose_name='رقم الهاتف')
    is_active = models.BooleanField(default=True, verbose_name='نشطة')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'مدرسة'
        verbose_name_plural = 'المدارس'
        ordering = ['name']

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    school = models.ForeignKey(School, on_delete=models.CASCADE, verbose_name='المدرسة')

    class Meta:
        verbose_name = 'ملف المستخدم'
        verbose_name_plural = 'ملفات المستخدمين'

    def __str__(self):
        return f'{self.user.username} - {self.school.name}'
