from django.urls import path
from django.contrib.auth.decorators import user_passes_test
from .views import TeacherDashboard

app_name = 'teachers'

staff_required=user_passes_test(lambda u: u.is_authenticated and (u.is_staff or u.is_superuser),login_url='/')

urlpatterns = [
    path('dashboard/', staff_required(TeacherDashboard.as_view()), name='teacher_dashboard'),
]
