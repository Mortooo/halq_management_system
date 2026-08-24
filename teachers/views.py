from datetime import date
from django.views.generic import ListView
from attendances.models import StudAttendance
from students.models import Student
from teachers.models import Teacher


class TeacherDashboard(ListView):
    template_name='teachers/teacher_dashboard.html'
    model=Student
    context_object_name='students'


    def get_context_data(self, **kwargs):

        context=super().get_context_data(**kwargs)
        # show the name of the teacher
        user=self.request.user
        teacher=Teacher.objects.filter(user_name=user).first()
        #show today date
        today=date.today()
        if teacher:
            # total number of students
            total_std=Student.objects.filter(halaqa__res_teacher=teacher).count()
            today_records=StudAttendance.objects.filter(student__halaqa__res_teacher=teacher,day=today)
            # today's attendance only (not lifetime)
            attend=today_records.filter(status=True).count()
            absent=today_records.filter(status=False).count()
            not_recorded=total_std-attend-absent
            # list of students taught by teacher
            list_stds=Student.objects.filter(halaqa__res_teacher=teacher).select_related('halaqa','grade').order_by('name')
        else:
            total_std=attend=absent=not_recorded=0
            list_stds=Student.objects.none()



        # add to context
        context['teacher']=teacher
        context['today_date']=today
        context['total_std']=total_std
        context['attended']=attend
        context['absent']=absent
        context['not_recorded']=not_recorded
        context['students']=list_stds



        return context
