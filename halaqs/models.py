from datetime import date, timedelta
from django.db import models
from django import forms



# Create your models here.

class Halaqa(models.Model):
    name =models.CharField(max_length=50,blank=False,null=False)
    res_teacher=models.ForeignKey('teachers.Teacher',on_delete=models.SET_NULL,null=True,blank=True)
    course=models.CharField(max_length=50,blank=False,null=False)
    notes=models.TextField(blank=True,null=True)
    
    @property
    def attend_today_list(self):
        from attendances.models import StudAttendance
        from students.models import Student
        
        today=date.today()
        students=Student.objects.filter(halaqa=self)
        attendance=StudAttendance.objects.filter(student__in=students)
        
        
        return attendance
        
    @property
    def total_students(self):
        
        from students.models import Student
        total=Student.objects.filter(halaqa=self).count()

        return total
    
    @property
    def total_absent_students(self):
        
        from attendances.models import StudAttendance
        from students.models import Student
        
        students=Student.objects.filter(halaqa=self)
        total=StudAttendance.objects.filter(student__in=students,day=date.today(),status=True).count()
        
        if not total:
            total=0
        
        return total
    
    
    @property
    def teacher_status(self):
        from teachers.models import Teacher
        teacher=self.res_teacher
        # status=Teacher.objects.get(teacher=teacher)
    
    @property
    def plan_status(self):
        from reports.models import WeekReport
        
        # Get the date of the end of week 
        today = date.today()
        week_end_day = 3
        days_until_thursday = week_end_day - today.weekday()
        if days_until_thursday < 0:
            days_until_thursday += 7

        end_of_week = today + timedelta(days=days_until_thursday)
        ###########################################################
        
        status=WeekReport.objects.get(halaqa=self,end_w_date=end_of_week).compare_plan
                    
        return status
    
    def __str__(self):
        return self.name