from django.urls import path
from .views import dashbord
from django.contrib.auth.decorators import login_required
urlpatterns = [
    path('dashbord',login_required(dashbord.as_view()),name='teacher_dashboard'),
]
