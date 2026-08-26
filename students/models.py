from django.db import models
from halaqs.models import Halaqa
from datetime import date
from teachers.models import Teacher

# Create your models here.
class Student(models.Model):
    name=models.CharField(max_length=100,blank=False,null=False)
    address=models.CharField(max_length=100,blank=False,null=False)
    tel=models.CharField(max_length=10,blank=False,null=False)
    date_birth=models.DateField(blank=False,null=False)
    halaqa=models.ForeignKey(Halaqa,on_delete=models.SET_NULL,blank=False,null=True)
    add_course=models.CharField(max_length=50,blank=True,null=True)
    grade=models.ForeignKey('students.Grade',on_delete=models.SET_NULL,blank=False,null=True)
    status=models.BooleanField(default=True)
    school=models.ForeignKey('schools.School',on_delete=models.CASCADE,null=True,blank=True)
    
    def __str__(self):
        return self.name
    
    @property
    def age(self):
        if self.date_birth:
            today = date.today()
            # حساب الفرق بين السنين مع مراعاة اليوم والشهر
            age = today.year - self.date_birth.year - (
                (today.month, today.day) < (self.date_birth.month, self.date_birth.day)
            )
            return age
        return None
    
    @property
    def basic_course(self):
        if self.halaqa:
            return self.halaqa.course
        return None
    
    @property
    def attendace_today(self):
        from attendances.models import StudAttendance
        record=StudAttendance.objects.filter(student=self,day=date.today()).first()
        
        if record is None:
            return None
        return record.status

    
class Grade(models.Model):
    name=models.CharField(max_length=50)
    school=models.ForeignKey('schools.School',on_delete=models.CASCADE,null=True,blank=True)
    
    def __str__(self):
        return self.name
    
