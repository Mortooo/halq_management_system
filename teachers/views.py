from datetime import date
from django.shortcuts import render
from django.views.generic import ListView
from attendances.models import StudAttendance
from students.models import Student
from teachers.models import Teacher
from halaqs.models import Halaqa

# Create your views here.


class dashbord(ListView):
    template_name='teacher_dashboard.html'
    model=Student
    context_object_name='students'
    
    
    def get_context_data(self, **kwargs):
        
        context=super().get_context_data(**kwargs)
        # show the name of the teacher 
        user=self.request.user
        teacher=Teacher.objects.get(user_name=user)  
        #show today date 
        today=date.today
        # total number of students 
        total_std=Student.objects.filter(halaqa__res_teacher=teacher).count()
        # total student attend and absent  
        attend=StudAttendance.objects.filter(student__halaqa__res_teacher=teacher,status=True).count()
        absent=StudAttendance.objects.filter(student__halaqa__res_teacher=teacher,status=False).count()
        # list of students taugth by teacher
        list_stds=Student.objects.filter(halaqa__res_teacher=teacher)
        
        
        
        
        
        
        
        
        # add to context  
        context['teacher']=teacher  
        context['today_date']=today  
        context['total_std']=total_std  
        context['attended']=attend  
        context['absent']=absent  
        context['students']=list_stds  
        
        
          
        
        return context
    
    