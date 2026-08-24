from django.contrib import admin
from django.urls import path,include
from halaqs.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home,name='home'),
    path('accounts/', include('allauth.urls')),
    path('superuser/', include('superuser.urls')),
    path('teacher/', include('teachers.urls')),
    path('student/', include('students.urls')),
    path('attendance/', include('attendances.urls')),
    path('report/', include('reports.urls')),
]
