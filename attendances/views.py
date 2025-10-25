from datetime import date
from django.shortcuts import redirect, render
from django.views.generic import ListView

from halaqs.models import Halaqa
from students.models import Student
from teachers.models import Teacher
from .models import StudAttendance,TeachAttendance
from django.contrib import messages




class StudentAttList(ListView):
    template_name='student_att.html'
    model=StudAttendance
    context_object_name='students_att'
    
    
       
    def get_queryset(self):
        
        queryset=super().get_queryset()
        #################### get the date and list of students #########################
        today=date.today()
        user=self.request.user
        students=Student.objects.filter(halaqa__res_teacher__user_name=user,status=True)
        ##############################################################################################
        queryset=queryset.filter(student__in=students,day=today)
        selected_halaqa=self.request.GET.get("selected_halaqa")
        
        if selected_halaqa:
            queryset=queryset.filter(student__halaqa__id=selected_halaqa)
            
        # when the teacher open attendace tab create attendance for every student with default true is attend 
        for student in students:
            if not StudAttendance.objects.filter(student=student,day=today).exists():
                StudAttendance.objects.create(student=student)
            

        return queryset
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        
        user=self.request.user
        halaqats=Halaqa.objects.filter(res_teacher__user_name=user)
        
        
        ###### add to context ####
        context['halaqats']=halaqats
        
        return context
    
    
    def post(self,request,*args, **kwargs):
        today=date.today()

        
        student_ids = request.POST.getlist('student_id')     
         
        for student_id in student_ids:
            student=Student.objects.get(id=student_id)
            status=request.POST.get(f'status_{student_id}')
            notes=request.POST.get(f'notes_{student_id}')
            
            StudAttendance.objects.update_or_create(
                student=student,
                defaults={
                'status': status,
                'notes': notes
                },
                day=today  
            )
            
            messages.success(request, "✅ تم حفظ السجلات بنجاح")

            
             
        return redirect(request.path)
    
class TeacherAttList(ListView):
    template_name='teacher_attendance.html'
    model=TeachAttendance
    context_object_name='teacher_att'
    

    
       
    def get_queryset(self):
        today=date.today()

        
        queryset=super().get_queryset()
        #################### get the date and list of students #########################
        teachers=Teacher.objects.all()
        ##############################################################################################
        queryset=queryset.filter(day=today)
            
        # when the teacher open attendace tab create attendance for every student with default true is attend 
        for teacher in teachers:
            if not TeachAttendance.objects.filter(teacher=teacher,day=today).exists():
                TeachAttendance.objects.create(teacher=teacher)
            

        return queryset
 
    
    def post(self,request,*args, **kwargs):
        today=date.today()

        
        teacher_ids = request.POST.getlist('teacher_id')     
         
        for teacher_id in teacher_ids:
            teacher=Teacher.objects.get(id=teacher_id)
            status=request.POST.get(f'status_{teacher_id}')
            notes=request.POST.get(f'notes_{teacher_id}')
            
            TeachAttendance.objects.update_or_create(
                teacher=teacher,
                defaults={
                'status': status,
                'notes': notes
                },
                day=today
            )
            
            messages.success(request, "✅ تم حفظ السجلات بنجاح")

            
             
        return redirect(request.path)
    
class AttendanceRecord(ListView):
    template_name='attendance_record.html'
    model=TeachAttendance
    context_object_name='teacher_att'
    
    def get_queryset(self):
        queryset=super().get_queryset()
        
        teacher=self.request.GET.get('teacher')
        start_date=self.request.GET.get('start_date')
        end_date=self.request.GET.get('end_date')
        
        if teacher:
            queryset=queryset.filter(teacher=teacher)
        
        if start_date and end_date:
            queryset=queryset.filter(day__range=[start_date,end_date])
        





        return queryset
    
   
    
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        
        teachers=Teacher.objects.all()
        
        
        context['teachers']=teachers
        
        
        
        return context
    
    
    