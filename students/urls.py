from django.urls import path
from .views import StudentsList,StudentCreate,StudentDetails,StudentUpdate,StudentDelete
from django.contrib.auth.decorators import login_required

app_name = 'students'

urlpatterns = [
    path('list/<int:pk>',login_required(StudentsList.as_view()),name='students_list'),
    path('add/',login_required(StudentCreate.as_view()),name='student_add'),
    path('details/<int:pk>',login_required(StudentDetails.as_view()),name='student_details'),
    path('update/<int:pk>',login_required(StudentUpdate.as_view()),name='student_update'),
    path('delete/<int:pk>',login_required(StudentDelete.as_view()),name='student_delete'),
]
