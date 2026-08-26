from core.access import superuser_with_school
from django.urls import path

from .views import dashboard ,TeacherList,TeacherCreate,TeacherUpdate,TeacherDelete,UsersList,HalaqaList,HalaqaCreate,HalaqaUpdate,HalaqaDelete,toggle_user_active,UserDelete

app_name = 'administration'


urlpatterns = [
    path('dashboard/' ,superuser_with_school(dashboard),name='dashboard'),
    path('teacher_list/' ,superuser_with_school(TeacherList.as_view()),name='teacher_list'),
    path('add/' ,superuser_with_school(TeacherCreate.as_view()),name='add_teacher'),
    path('delete/<int:pk>/' ,superuser_with_school(TeacherDelete.as_view()),name='delete_teacher'),
    path('update/<int:pk>/' ,superuser_with_school(TeacherUpdate.as_view()),name='edit_teacher'),
    path('halaqa_list/', superuser_with_school(HalaqaList.as_view()), name='halaqa_list'),
    path('halaqa/add/', superuser_with_school(HalaqaCreate.as_view()), name='add_halaqa'),
    path('halaqa/delete/<int:pk>/', superuser_with_school(HalaqaDelete.as_view()), name='delete_halaqa'),
    path('halaqa/update/<int:pk>/', superuser_with_school(HalaqaUpdate.as_view()), name='edit_halaqa'),
    path('users/', superuser_with_school(UsersList.as_view()), name='users_list'),
    path('users/<int:pk>/toggle/', superuser_with_school(toggle_user_active), name='toggle_user'),
    path('users/<int:pk>/delete/', superuser_with_school(UserDelete.as_view()), name='delete_user'),
]
