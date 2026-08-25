from halq_management_system.access import staff_required
from django.urls import path
from .views import TeacherDashboard

app_name = 'teachers'


urlpatterns = [
    path('dashboard/', staff_required(TeacherDashboard.as_view()), name='teacher_dashboard'),
]
