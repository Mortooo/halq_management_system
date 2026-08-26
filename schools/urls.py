from django.urls import path
from .views import SchoolListView, SchoolCreateView, SchoolUpdateView, SchoolDeleteView, AssignSchoolUserView, RegisterSchoolView

app_name = 'schools'

urlpatterns = [
    path('', SchoolListView.as_view(), name='school_list'),
    path('add/', SchoolCreateView.as_view(), name='school_add'),
    path('register/', RegisterSchoolView.as_view(), name='register_school'),
    path('<int:pk>/edit/', SchoolUpdateView.as_view(), name='school_edit'),
    path('<int:pk>/delete/', SchoolDeleteView.as_view(), name='school_delete'),
    path('<int:school_id>/users/', AssignSchoolUserView.as_view(), name='school_users'),
]
