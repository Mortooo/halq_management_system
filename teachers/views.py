from datetime import date
from django.views.generic import ListView
from attendances.models import StudAttendance
from students.models import Student
from teachers.models import Teacher


class TeacherDashboard(ListView):
    template_name='teachers/teacher_dashboard.html'
    model=Student
    context_object_name='students'

    def get_queryset(self):
        user=self.request.user
        teacher=Teacher.objects.filter(user_name=user).first()
        if teacher:
            return Student.objects.filter(halaqa__res_teacher=teacher,school=self.request.school).select_related('halaqa','grade').order_by('name')
        return Student.objects.none()

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        user=self.request.user
        teacher=Teacher.objects.filter(user_name=user).first()
        today=date.today()
        school=self.request.school
        if teacher:
            total_std=Student.objects.filter(halaqa__res_teacher=teacher,school=school).count()
            today_records=StudAttendance.objects.filter(student__halaqa__res_teacher=teacher,student__school=school,day=today)
            attend=today_records.filter(status=True).count()
            absent=today_records.filter(status=False).count()
            recorded=attend+absent
            att_percent=round(attend/recorded*100) if recorded else 0
        else:
            total_std=attend=absent=0
            att_percent=0

        context['teacher']=teacher
        context['today_date']=today
        context['total_std']=total_std
        context['attended']=attend
        context['absent']=absent
        context['att_percent']=att_percent
        return context
