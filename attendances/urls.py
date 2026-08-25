from core.access import staff_required, superuser_required
from django.urls import path
from .views import StudentAttList,TeacherAttList,AttendanceRecord,StudentRecord

app_name = 'attendances'


urlpatterns = [
    path('students/<int:pk>/',staff_required(StudentAttList.as_view()),name='student_attendance'),
    path('teachers/',superuser_required(TeacherAttList.as_view()),name='teacher_attendance'),
    path('records/',superuser_required(AttendanceRecord.as_view()),name='attendance_record'),
    path('records/students/',superuser_required(StudentRecord.as_view()),name='student_records'),
]
