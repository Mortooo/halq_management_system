from django.urls import reverse
from allauth.account.adapter import DefaultAccountAdapter
from schools.models import UserProfile


class MyAccountAdapter(DefaultAccountAdapter):

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

