from core.access import staff_with_school
from django.urls import path
from .views import TeacherDashboard

app_name = 'teachers'


urlpatterns = [
    path('dashboard/', staff_with_school(TeacherDashboard.as_view()), name='teacher_dashboard'),
]
