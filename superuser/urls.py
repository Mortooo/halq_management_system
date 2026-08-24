from django.urls import path

from .views import dashbord ,TeacherList,TeacherCreate,TeacherUpdate,TeacherDelete,UsersList,HalaqaList,HalaqaCreate,HalaqaUpdate,HalaqaDelete
from django.contrib.auth.decorators import user_passes_test

app_name = 'superuser'

superuser_required=user_passes_test(lambda u: u.is_authenticated and u.is_superuser,login_url='/')

urlpatterns = [
    path('dashboard' ,superuser_required(dashbord),name='dashboard'),
    path('teacher_list/' ,superuser_required(TeacherList.as_view()),name='teacher_list'),
    path('add/' ,superuser_required(TeacherCreate.as_view()),name='add_teacher'),
    path('delete/<int:pk>' ,superuser_required(TeacherDelete.as_view()),name='delete_teacher'),
    path('update/<int:pk>' ,superuser_required(TeacherUpdate.as_view()),name='edit_teacher'),
    # Halaqa management
    path('halaqa_list/', superuser_required(HalaqaList.as_view()), name='halaqa_list'),
    path('halaqa/add/', superuser_required(HalaqaCreate.as_view()), name='add_halaqa'),
    path('halaqa/delete/<int:pk>/', superuser_required(HalaqaDelete.as_view()), name='delete_halaqa'),
    path('halaqa/update/<int:pk>/', superuser_required(HalaqaUpdate.as_view()), name='edit_halaqa'),
    # users
    path('users/' ,superuser_required(UsersList.as_view()),name='users_list'),
    path('users/add' ,superuser_required(UsersList.as_view()),name='add_user'),
]
