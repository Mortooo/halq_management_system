from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('accounts/', include('allauth.urls')),
    path('superuser/', include('superuser.urls')),
    path('teacher/', include('teachers.urls')),
    path('student/', include('students.urls')),
    path('attendance/', include('attendances.urls')),
    path('report/', include('reports.urls')),
]
