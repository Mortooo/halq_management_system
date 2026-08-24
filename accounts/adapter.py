from django.urls import reverse
from allauth.account.adapter import DefaultAccountAdapter

class MyAccountAdapter(DefaultAccountAdapter):
    
     def get_login_redirect_url(self, request):
        user = request.user
        if user.is_superuser:
            return reverse('superuser:dashboard')
        elif user.is_staff:
            return reverse('teachers:teacher_dashboard')
        return reverse('home')

