from django.urls import path

from attendances.views import TeacherAttList,AttendanceRecord
from reports.views import TotalReport,ReportDetails
from .views import dashbord ,TeacherList,TeacherCreate,TeacherUpdate,TeacherDelete
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('dashborad' ,dashbord,name='superuser_dashboard'),
    path('teacher_list/' ,login_required(TeacherList.as_view()),name='teacher_list'),
    path('add/' ,login_required(TeacherCreate.as_view()),name='add_teacher'),
    path('delete/<int:pk>' ,login_required(TeacherDelete.as_view()),name='delete_teacher'),
    path('update/<int:pk>' ,login_required(TeacherUpdate.as_view()),name='edit_teacher'),
    # Halaqa management
    path('halaqa_list/', login_required(__import__('superuser.views', fromlist=['']).HalaqaList.as_view()), name='halaqa_list'),
    path('halaqa/add/', login_required(__import__('superuser.views', fromlist=['']).HalaqaCreate.as_view()), name='add_halaqa'),
    path('halaqa/delete/<int:pk>/', login_required(__import__('superuser.views', fromlist=['']).HalaqaDelete.as_view()), name='delete_halaqa'),
    path('halaqa/update/<int:pk>/', login_required(__import__('superuser.views', fromlist=['']).HalaqaUpdate.as_view()), name='edit_halaqa'),
    # attendance
    path('attendance/' ,login_required(TeacherAttList.as_view()),name='teacher_attendance'),
    path('reports/' ,login_required(TotalReport.as_view()),name='total_reports'),
    path('report_details/<int:pk>' ,login_required(ReportDetails.as_view()),name='report_details'),
    path('attendance_record' ,login_required(AttendanceRecord.as_view()),name='attendance_record'),

    
]
