from django.urls import path
# from .views import StudentsList,StudentCreate,StudentDetails,StudentUpdate,StudentDelete,StudentAttList
from django.contrib.auth.decorators import login_required
from .views import show_weekly_report

urlpatterns = [
   
    path('weekly_report/<int:pk>',login_required(show_weekly_report),name='weekly_report'),
    
]
