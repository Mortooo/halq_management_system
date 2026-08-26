from schools.models import UserProfile
from teachers.models import Teacher


class SchoolMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.school = None

        if request.user.is_authenticated:
            if request.user.is_superuser:
                profile = UserProfile.objects.filter(user=request.user).first()
                request.school = profile.school if profile else None
            else:
                teacher = Teacher.objects.filter(user_name=request.user).select_related('school').first()
                request.school = teacher.school if teacher else None

        response = self.get_response(request)
        return response
