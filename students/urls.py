from django.urls import path
from .views import StudentsList,StudentCreate,StudentDetails,StudentUpdate,StudentDelete,StudentAttList
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('list/<int:pk>',login_required(StudentsList.as_view()),name='students_list'),
    path('add/<int:pk>',login_required(StudentCreate.as_view()),name='student_add'),
    path('add/',login_required(StudentCreate.as_view()),name='student_add'),
    path('details/<int:pk>',login_required(StudentDetails.as_view()),name='student_details'),
    path('update/<int:pk>',login_required(StudentUpdate.as_view()),name='student_update'),
    path('delete/<int:pk>',login_required(StudentDelete.as_view()),name='student_delete'),
    path('students_attendance/<int:pk>',login_required(StudentAttList.as_view()),name='students_attendance'),
    
]
