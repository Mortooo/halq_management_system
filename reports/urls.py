from django.urls import path
from django.contrib.auth.decorators import user_passes_test
from .views import show_weekly_report, TotalReport, ReportDetails

app_name = 'reports'

superuser_required = user_passes_test(lambda u: u.is_authenticated and u.is_superuser, login_url='/')
staff_required = user_passes_test(lambda u: u.is_authenticated and (u.is_staff or u.is_superuser), login_url='/')

urlpatterns = [
    path('weekly_report/', staff_required(show_weekly_report), name='weekly_report'),
    path('list/', superuser_required(TotalReport.as_view()), name='total_reports'),
    path('details/<int:pk>/', superuser_required(ReportDetails.as_view()), name='report_details'),
]
