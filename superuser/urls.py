from django.urls import path
from .views import dashbord

urlpatterns = [
    path('dashborad' ,dashbord,name='superuser_dashboard')
]
