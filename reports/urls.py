from core.access import staff_with_school, superuser_with_school
from django.urls import path
from .views import show_weekly_report, TotalReport, ReportDetails

app_name = 'reports'


urlpatterns = [
    path('weekly_report/', staff_with_school(show_weekly_report), name='weekly_report'),
    path('list/', superuser_with_school(TotalReport.as_view()), name='total_reports'),
    path('details/<int:pk>/', superuser_with_school(ReportDetails.as_view()), name='report_details'),
]
