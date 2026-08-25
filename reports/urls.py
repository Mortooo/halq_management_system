from halq_management_system.access import staff_required, superuser_required
from django.urls import path
from .views import show_weekly_report, TotalReport, ReportDetails

app_name = 'reports'


urlpatterns = [
    path('weekly_report/', staff_required(show_weekly_report), name='weekly_report'),
    path('list/', superuser_required(TotalReport.as_view()), name='total_reports'),
    path('details/<int:pk>/', superuser_required(ReportDetails.as_view()), name='report_details'),
]
