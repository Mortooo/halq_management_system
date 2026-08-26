from core.access import staff_with_school, superuser_with_school
from django.urls import path
from .views import StudentAttList,TeacherAttList,AttendanceRecord,StudentRecord

app_name = 'attendances'


urlpatterns = [
    path('students/<int:pk>/',staff_with_school(StudentAttList.as_view()),name='student_attendance'),
    path('teachers/',superuser_with_school(TeacherAttList.as_view()),name='teacher_attendance'),
    path('records/',superuser_with_school(AttendanceRecord.as_view()),name='attendance_record'),
    path('records/students/',superuser_with_school(StudentRecord.as_view()),name='student_records'),
]
