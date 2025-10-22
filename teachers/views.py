from django.shortcuts import render
from django.views.generic import ListView
from students.models import Student

# Create your views here.


class dashbord(ListView):
    template_name='teacher_dashboard.html'
    model=Student
    context_object_name='students'
    
    