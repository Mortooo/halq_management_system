from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from schools.models import UserProfile
from teachers.models import Teacher


class SchoolMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.school = None

        if request.user.is_authenticated:
            if request.user.is_superuser:
                profile = UserProfile.objects.filter(user=request.user).select_related('school').first()
                request.school = profile.school if profile else None
            else:
                teacher = Teacher.objects.filter(user_name=request.user).select_related('school').first()
                request.school = teacher.school if teacher else None

            if request.school and not request.school.is_active:
                logout_url = reverse('account_logout')
                login_url = reverse('account_login')
                if request.path != logout_url and not request.path.startswith('/static/'):
                    logout(request)
                    messages.error(request, 'تم تعطيل حساب هذه المدرسة من قبل الإدارة العامة. يرجى التواصل مع إدارة النظام.')
                    return redirect(login_url)

        response = self.get_response(request)
        return response

