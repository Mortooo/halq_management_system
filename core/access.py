from functools import wraps
from django.contrib.auth.decorators import user_passes_test
from django.http import Http404


def school_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(request.get_full_path())
        if not request.school or not request.school.is_active:
            raise Http404()
        return view_func(request, *args, **kwargs)
    return wrapper


def _staff_test(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)


def _superuser_test(user):
    return user.is_authenticated and user.is_superuser


staff_required = user_passes_test(_staff_test, login_url='/')

superuser_required = user_passes_test(_superuser_test, login_url='/')


def staff_with_school(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not _staff_test(request.user):
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(request.get_full_path())
        if not request.school or not request.school.is_active:
            raise Http404()
        return view_func(request, *args, **kwargs)
    return wrapper


def superuser_with_school(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not _superuser_test(request.user):
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(request.get_full_path())
        if not request.school or not request.school.is_active:
            raise Http404()
        return view_func(request, *args, **kwargs)
    return wrapper

