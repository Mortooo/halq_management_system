from django.urls import path
from .views import dashbord
from django.contrib.auth.decorators import login_required

app_name = 'teachers'

urlpatterns = [
    path('dashboard', login_required(dashbord.as_view()), name='teacher_dashboard'),
]
