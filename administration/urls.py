from halq_management_system.access import superuser_required
from django.urls import path

from .views import dashboard ,TeacherList,TeacherCreate,TeacherUpdate,TeacherDelete,UsersList,HalaqaList,HalaqaCreate,HalaqaUpdate,HalaqaDelete,toggle_user_active,UserDelete

app_name = 'administration'


urlpatterns = [
    path('dashboard/' ,superuser_required(dashboard),name='dashboard'),
    path('teacher_list/' ,superuser_required(TeacherList.as_view()),name='teacher_list'),
    path('add/' ,superuser_required(TeacherCreate.as_view()),name='add_teacher'),
    path('delete/<int:pk>/' ,superuser_required(TeacherDelete.as_view()),name='delete_teacher'),
    path('update/<int:pk>/' ,superuser_required(TeacherUpdate.as_view()),name='edit_teacher'),
    # Halaqa management
    path('halaqa_list/', superuser_required(HalaqaList.as_view()), name='halaqa_list'),
    path('halaqa/add/', superuser_required(HalaqaCreate.as_view()), name='add_halaqa'),
    path('halaqa/delete/<int:pk>/', superuser_required(HalaqaDelete.as_view()), name='delete_halaqa'),
    path('halaqa/update/<int:pk>/', superuser_required(HalaqaUpdate.as_view()), name='edit_halaqa'),
    # users
    path('users/', superuser_required(UsersList.as_view()), name='users_list'),
    path('users/<int:pk>/toggle/', superuser_required(toggle_user_active), name='toggle_user'),
    path('users/<int:pk>/delete/', superuser_required(UserDelete.as_view()), name='delete_user'),
]
