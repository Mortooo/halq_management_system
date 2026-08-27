import os
from django.conf import settings
from django.http import HttpResponse, FileResponse
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib import admin


def service_worker(request):
    sw_path = os.path.join(settings.BASE_DIR, 'static', 'sw.js')
    with open(sw_path, 'r', encoding='utf-8') as f:
        return HttpResponse(f.read(), content_type='application/javascript')


def manifest_view(request):
    manifest_path = os.path.join(settings.BASE_DIR, 'static', 'manifest.json')
    with open(manifest_path, 'r', encoding='utf-8') as f:
        return HttpResponse(f.read(), content_type='application/manifest+json')


def download_apk(request):
    apk_path = os.path.join(settings.BASE_DIR, 'إدارة الحلقات.apk')
    if os.path.exists(apk_path):
        return FileResponse(open(apk_path, 'rb'), as_attachment=True, filename='adminstration.apk')
    return HttpResponse('الملف غير موجود', status=404)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('sw.js', service_worker, name='service_worker'),
    path('manifest.json', manifest_view, name='manifest'),
    path('download-apk/', download_apk, name='download_apk'),
    path('accounts/', include('allauth.urls')),
    path('schools/', include('schools.urls')),
    path('administration/', include('administration.urls')),
    path('teacher/', include('teachers.urls')),
    path('student/', include('students.urls')),
    path('attendance/', include('attendances.urls')),
    path('report/', include('reports.urls')),
]

