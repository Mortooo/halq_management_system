from datetime import date
from django.shortcuts import render
from django.urls import reverse_lazy

from halaqs.models import Halaqa
from students.models import Student
from django.views.generic import ListView,CreateView,UpdateView,DeleteView

from superuser.forms import TeacherForm
from teachers.models import Teacher

# Create your views here.

def dashbord(request):
    
    today_date=date.today()# get today date 
    user=request.user.first_name # user is log in 
    total_halaqats=Halaqa.objects.all().count()
    total_students=Student.objects.all().count()
    halaqats=Halaqa.objects.all() 
    #################### add to context #####################
    context ={
        'today_date':today_date,
        'user' :user,
        'total_halaqats':total_halaqats,
        'total_students':total_students,
        'halaqats':halaqats
    }
    
    
    
    return render(request,'superuser_dashboard.html',context)


class TeacherList(ListView):
    model=Teacher
    template_name='teacher_manage.html'
    context_object_name='teachers'
    
    def get_queryset(self):
        query=super().get_queryset()
        
        if self.request.GET.get('q'):
            name=self.request.GET.get('q').rstrip()
            query=query.filter(name__icontains=name)
        
        
        
        
        return query

class TeacherCreate(CreateView):
    template_name='teacher_add.html'
    model=Teacher
    form_class=TeacherForm
    success_url=reverse_lazy('teacher_list')
    
class TeacherUpdate(UpdateView):
    template_name='teacher_add.html'
    model=Teacher
    form_class=TeacherForm
    success_url=reverse_lazy('teacher_list')
    
class TeacherDelete(DeleteView):
    template_name='teacher_delete.html'
    model=Teacher
    success_url=reverse_lazy('teacher_list')
    

class HalaqaList(ListView):
    model=Halaqa
    template_name='halaqa_manage.html'
    context_object_name='halaqats'

    def get_queryset(self):
        query=super().get_queryset()
        if self.request.GET.get('q'):
            name=self.request.GET.get('q').rstrip()
            query=query.filter(name__icontains=name)

        return query


class HalaqaCreate(CreateView):
    template_name='halaqa_add.html'
    model=Halaqa
    fields=['name','res_teacher','course','notes']
    success_url=reverse_lazy('halaqa_list')


class HalaqaUpdate(UpdateView):
    template_name='halaqa_add.html'
    model=Halaqa
    fields=['name','res_teacher','course','notes']
    success_url=reverse_lazy('halaqa_list')

class HalaqaDelete(DeleteView):
    template_name='halaqa_delete.html'
    model=Halaqa
    context_object_name='halaqa'
    success_url=reverse_lazy('halaqa_list')


    
    
 
