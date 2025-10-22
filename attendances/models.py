from django.db import models
from students.models import Student
from teachers.models import Teacher
from datetime import date


# Create your models here.
class StudAttendance(models.Model):
    student=models.ForeignKey('students.Student',on_delete=models.CASCADE)
    day=models.DateField(default=date.today)
    status=models.BooleanField(default=True)
    notes=models.TextField(blank=True,null=True)
    
    def __str__(self):
        
        return f'att for {self.student} on date {self.day}  '

class TeachAttendance(models.Model):
    teacher=models.ForeignKey(Teacher,on_delete=models.CASCADE)
    day=models.DateField(default=date.today)
    status=models.BooleanField(default=True)
    notes=models.TextField(blank=True,null=True)