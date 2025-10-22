from django.shortcuts import render
from django.views.generic import ListView
from .models import StudAttendance,TeachAttendance

# Create your views here.
class StudentAttList(ListView):
    template_name=''
    model=
    
