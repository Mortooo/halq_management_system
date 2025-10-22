from django.shortcuts import redirect, render
from django.views.generic import ListView,CreateView,UpdateView,DeleteView,DetailView
from students.models import Student
from teachers.models import Teacher
from halaqs.models import Halaqa
from .forms import StudentForm
from django.urls import reverse_lazy
from django.db.models import Q
from attendances.models import StudAttendance
from datetime import date
from django.contrib import messages
# Create your views here.

class StudentsList(ListView):
    template_name='students_list.html'
    model=Student
    context_object_name='students'
    
    def get_queryset(self):
        
        print('we are here ')
        # get the current login user asume he is teacher not supervisor 
        teacher=Teacher.objects.get(user_name=self.kwargs.get('pk'))

        # get list of all students 
        students=Student.objects.all()
        # get list of halaqats teacher is teach 
        halaqats=Halaqa.objects.filter(res_teacher=teacher)

        # finallay get the student are in reading in these halaqats 
        
        students=Student.objects.filter(halaqa__in=halaqats)
        #######################################################################################
        # if the user search for some student or halaqats
        if self.request.GET.get('q'):
            students=students.filter(Q(name__icontains=self.request.GET.get('q'))|Q(halaqa__name__icontains=self.request.GET.get('q')))
            
        
        return students
    
class StudentCreate(CreateView):
    template_name='student_add.html'
    model=Student
    form_class=StudentForm
    
   
    def get_success_url(self):
       
        return reverse_lazy('students_list', kwargs={'pk': self.request.user.id})
    
    
    
class StudentUpdate(UpdateView):
    template_name='student_add.html'
    model=Student
    form_class=StudentForm
    
    def get_success_url(self):
       
        return reverse_lazy('students_list', kwargs={'pk': self.request.user.id})
    
    
class StudentDetails(DetailView):
    template_name='student_detail.html'
    model=Student
    
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        student_id=self.kwargs.get('pk')
        
        attenedance_list=StudAttendance.objects.filter(student__id=student_id)
        
        #calculate the attendance percantege 
        total_days=len(attenedance_list)
        attend_days=len(attenedance_list.filter(status=True))
        
        attend_percantage=0
        if not attend_days==0:
            attend_percantage=attend_days/total_days*100
   
        
        
        context['attenedance_list']=attenedance_list
        context['attend_percantage']=attend_percantage
        
        
        
        return context
    
class StudentDelete(DeleteView):
    template_name='student_delete.html'
    model=Student
    
    def get_success_url(self):
       
        return reverse_lazy('students_list', kwargs={'pk': self.request.user.id})
    
# Create your views here.
class StudentAttList(ListView):
    template_name='student_att.html'
    model=StudAttendance
    context_object_name='students_att'
    
       
    
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        
        ###################(stage 1)##########################
        # get the user is log in
        user=self.kwargs.get('pk')
        # get the teacher with user creidentions
        teacher=Teacher.objects.get(user_name_id=user)
        # get the list halaqat the teacher teach
        halaqats=Halaqa.objects.filter(res_teacher=teacher)
        # get studets whom are teached the the teacher 
        students=Student.objects.filter(halaqa__in=halaqats)
        ###################(stage 2)##########################
        # create attendance record for every students whom has no record for today 
        current_date=date.today()
        for student in students:
            if not StudAttendance.objects.filter(student=student,day=current_date).exists():
                StudAttendance.objects.create(student=student)

        return context
    
    def post(self,request,*args, **kwargs):
        
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
                }  
            )
            
             
        return redirect(request.path)
        # return self.render_to_response(context)
    
    
    

        
