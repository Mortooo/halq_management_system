from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from allauth.account.adapter import DefaultAccountAdapter
try:
    from allauth.core.exceptions import ImmediateHttpResponse
except ImportError:
    from allauth.exceptions import ImmediateHttpResponse
from schools.models import UserProfile
from teachers.models import Teacher


class MyAccountAdapter(DefaultAccountAdapter):

    def pre_login(self, request, user, **kwargs):
        school = None
        if user.is_superuser:
            profile = UserProfile.objects.filter(user=user).select_related('school').first()
            if profile:
                school = profile.school
        else:
            teacher = Teacher.objects.filter(user_name=user).select_related('school').first()
            if teacher:
                school = teacher.school

        if school and not school.is_active:
            messages.error(request, 'تم تعطيل حساب هذه المدرسة من قبل الإدارة العامة. يرجى التواصل مع إدارة النظام.')
            raise ImmediateHttpResponse(redirect('account_login'))

        return super().pre_login(request, user, **kwargs)

    def get_login_redirect_url(self, request):
        user = request.user
        if user.is_superuser:
            profile = UserProfile.objects.filter(user=user).first()
            if profile and profile.school:
                return reverse('administration:dashboard')
            return reverse('schools:school_list')
        elif user.is_staff:
            return reverse('teachers:teacher_dashboard')
        return reverse('home')

    def get_password_change_redirect_url(self, request):
        return self.get_login_redirect_url(request)



