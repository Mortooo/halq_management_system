from django.shortcuts import redirect, render
from django.views.generic import ListView,CreateView,UpdateView,DeleteView,DetailView
from django.http import Http404
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

class TeacherOwnedStudentMixin:
    def dispatch(self, request, *args, **kwargs):
        obj=self.get_object()
        teacher=obj.halaqa.res_teacher if obj.halaqa else None
        owner=teacher.user_name if teacher else None
        if not request.user.is_superuser and owner!=request.user:
            raise Http404()
        return super().dispatch(request,*args,**kwargs)

class StudentsList(ListView):
    template_name='students/students_list.html'
    model=Student
    context_object_name='students'

    def get_queryset(self):

        pk=self.kwargs.get('pk')
        if not self.request.user.is_superuser and self.request.user.id != pk:
            raise Http404()
        # get the current login user asume he is teacher not supervisor
        teacher=Teacher.objects.filter(user_name_id=pk).first()
        if teacher is None:
            return Student.objects.none()

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
    template_name='students/student_add.html'
    model=Student
    form_class=StudentForm
    
   
    def get_success_url(self):
       
        return reverse_lazy('students:students_list', kwargs={'pk': self.request.user.id})
    
    
    
class StudentUpdate(TeacherOwnedStudentMixin,UpdateView):
    template_name='students/student_add.html'
    model=Student
    form_class=StudentForm
    
    def get_success_url(self):
       
        return reverse_lazy('students:students_list', kwargs={'pk': self.request.user.id})
    
    
class StudentDetails(TeacherOwnedStudentMixin,DetailView):
    template_name='students/student_detail.html'
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
    
class StudentDelete(TeacherOwnedStudentMixin,DeleteView):
    template_name='students/student_delete.html'
    model=Student
    
    def get_success_url(self):
       
        return reverse_lazy('students:students_list', kwargs={'pk': self.request.user.id})
    
