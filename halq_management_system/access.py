from django.contrib.auth.decorators import user_passes_test

staff_required = user_passes_test(
    lambda u: u.is_authenticated and (u.is_staff or u.is_superuser),
    login_url='/',
)

superuser_required = user_passes_test(
    lambda u: u.is_authenticated and u.is_superuser,
    login_url='/',
)
