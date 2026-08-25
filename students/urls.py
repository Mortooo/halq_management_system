from halq_management_system.access import staff_required, superuser_required
from django.urls import path
from .views import StudentsList,StudentCreate,StudentDetails,StudentUpdate,StudentDelete,SUStudentList,SUStudentCreate,SUStudentUpdate,SUStudentDelete,SUGradeList,SUGradeCreate,SUGradeUpdate,SUGradeDelete

app_name = 'students'


urlpatterns = [
    path('list/<int:pk>/',staff_required(StudentsList.as_view()),name='students_list'),
    path('add/',staff_required(StudentCreate.as_view()),name='student_add'),
    path('details/<int:pk>/',staff_required(StudentDetails.as_view()),name='student_details'),
    path('update/<int:pk>/',staff_required(StudentUpdate.as_view()),name='student_update'),
    path('delete/<int:pk>/',staff_required(StudentDelete.as_view()),name='student_delete'),
    path('manage/',superuser_required(SUStudentList.as_view()),name='students_manage'),
    path('manage/add/',superuser_required(SUStudentCreate.as_view()),name='student_add_su'),
    path('manage/update/<int:pk>/',superuser_required(SUStudentUpdate.as_view()),name='student_edit_su'),
    path('manage/delete/<int:pk>/',superuser_required(SUStudentDelete.as_view()),name='student_delete_su'),
    path('grade/manage/',superuser_required(SUGradeList.as_view()),name='grade_manage'),
    path('grade/manage/add/',superuser_required(SUGradeCreate.as_view()),name='grade_add_su'),
    path('grade/manage/update/<int:pk>/',superuser_required(SUGradeUpdate.as_view()),name='grade_edit_su'),
    path('grade/manage/delete/<int:pk>/',superuser_required(SUGradeDelete.as_view()),name='grade_delete_su'),
]
