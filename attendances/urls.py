from django.urls import path
from django.contrib.auth.decorators import login_required, user_passes_test
from .views import StudentAttList,TeacherAttList,AttendanceRecord

app_name = 'attendances'

superuser_required=user_passes_test(lambda u: u.is_authenticated and u.is_superuser,login_url='/')

urlpatterns = [
    path('students/<int:pk>',login_required(StudentAttList.as_view()),name='student_attendance'),
    path('teachers/',superuser_required(TeacherAttList.as_view()),name='teacher_attendance'),
    path('records/',superuser_required(AttendanceRecord.as_view()),name='attendance_record'),
]
