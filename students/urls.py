from core.access import staff_with_school, superuser_with_school
from django.urls import path
from .views import StudentsList,StudentCreate,StudentDetails,StudentUpdate,StudentDelete,SUStudentList,SUStudentCreate,SUStudentUpdate,SUStudentDelete,SUGradeList,SUGradeCreate,SUGradeUpdate,SUGradeDelete

app_name = 'students'


urlpatterns = [
    path('list/<int:pk>/',staff_with_school(StudentsList.as_view()),name='students_list'),
    path('add/',staff_with_school(StudentCreate.as_view()),name='student_add'),
    path('details/<int:pk>/',staff_with_school(StudentDetails.as_view()),name='student_details'),
    path('update/<int:pk>/',staff_with_school(StudentUpdate.as_view()),name='student_update'),
    path('delete/<int:pk>/',staff_with_school(StudentDelete.as_view()),name='student_delete'),
    path('manage/',superuser_with_school(SUStudentList.as_view()),name='students_manage'),
    path('manage/add/',superuser_with_school(SUStudentCreate.as_view()),name='student_add_su'),
    path('manage/update/<int:pk>/',superuser_with_school(SUStudentUpdate.as_view()),name='student_edit_su'),
    path('manage/delete/<int:pk>/',superuser_with_school(SUStudentDelete.as_view()),name='student_delete_su'),
    path('grade/manage/',superuser_with_school(SUGradeList.as_view()),name='grade_manage'),
    path('grade/manage/add/',superuser_with_school(SUGradeCreate.as_view()),name='grade_add_su'),
    path('grade/manage/update/<int:pk>/',superuser_with_school(SUGradeUpdate.as_view()),name='grade_edit_su'),
    path('grade/manage/delete/<int:pk>/',superuser_with_school(SUGradeDelete.as_view()),name='grade_delete_su'),
]
