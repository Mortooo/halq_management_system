from django.shortcuts import redirect
from django.views.generic import ListView,CreateView,UpdateView,DeleteView,DetailView
from django.http import Http404
from students.models import Student, Grade
from .forms import StudentForm, GradeForm
from django.urls import reverse
from django.db.models import Q
from attendances.models import StudAttendance
from django.contrib import messages

class TeacherOwnedStudentMixin:
    def dispatch(self, request, *args, **kwargs):
        obj=self.get_object()
        teacher=obj.halaqa.res_teacher if obj.halaqa else None
        owner=teacher.user_name if teacher else None
        if not request.user.is_superuser and owner!=request.user:
            raise Http404()
        return super().dispatch(request,*args,**kwargs)

    def get_object(self, queryset=None):
        # cache so the object is fetched once per request (dispatch + CBV internals)
        if getattr(self, '_object_cache', None) is None:
            self._object_cache=super().get_object(queryset)
        return self._object_cache

class UserFormKwargsMixin:
    def get_form_kwargs(self):
        kwargs=super().get_form_kwargs()
        kwargs['user']=self.request.user
        return kwargs

class StudentsList(ListView):
    template_name='students/students_list.html'
    model=Student
    context_object_name='students'
    paginate_by=15

    def get_queryset(self):

        pk=self.kwargs.get('pk')
        if self.request.user.is_superuser:
            # superuser sees every student in the system
            students=Student.objects.select_related('halaqa','grade').all()
        else:
            if self.request.user.id != pk:
                raise Http404()
            students=Student.objects.filter(halaqa__res_teacher__user_name_id=pk).select_related('halaqa','grade')

        #######################################################################################
        # if the user search for some student or halaqats
        if self.request.GET.get('q'):
            students=students.filter(Q(name__icontains=self.request.GET.get('q'))|Q(halaqa__name__icontains=self.request.GET.get('q')))


        return students.order_by('name')


class StudentCreate(UserFormKwargsMixin,CreateView):
    template_name='students/student_add.html'
    model=Student
    form_class=StudentForm


    def get_success_url(self):

        return reverse('students:students_list', kwargs={'pk': self.request.user.id})



class StudentUpdate(TeacherOwnedStudentMixin,UserFormKwargsMixin,UpdateView):
    template_name='students/student_add.html'
    model=Student
    form_class=StudentForm

    def get_success_url(self):

        return reverse('students:students_list', kwargs={'pk': self.request.user.id})


class StudentDetails(TeacherOwnedStudentMixin,DetailView):
    template_name='students/student_detail.html'
    model=Student


    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        student_id=self.kwargs.get('pk')

        all_records=StudAttendance.objects.filter(student__id=student_id).order_by('-day')
        attendance_list=all_records[:10]

        #calculate the attendance percantege
        total_days=all_records.count()
        attend_days=all_records.filter(status=True).count()

        attend_percantage=(attend_days/total_days*100) if total_days else 0



        context['attendance_list']=attendance_list
        context['attendance_count']=total_days
        context['attend_percantage']=round(attend_percantage,1)



        return context

class StudentDelete(TeacherOwnedStudentMixin,DeleteView):
    template_name='students/student_delete.html'
    model=Student

    def get_success_url(self):

        return reverse('students:students_list', kwargs={'pk': self.request.user.id})


# ---------- Superuser-side management (all students) ----------

class SUStudentList(ListView):
    template_name='superuser/students_manage.html'
    model=Student
    context_object_name='students'
    paginate_by=15

    def get_queryset(self):
        students=Student.objects.select_related('halaqa','grade').all()
        q=self.request.GET.get('q')
        if q:
            students=students.filter(Q(name__icontains=q)|Q(halaqa__name__icontains=q))
        return students.order_by('name')


class SUStudentCreate(UserFormKwargsMixin,CreateView):
    template_name='superuser/student_edit.html'
    model=Student
    form_class=StudentForm

    def get_success_url(self):
        return reverse('students:students_manage')


class SUStudentUpdate(TeacherOwnedStudentMixin,UserFormKwargsMixin,UpdateView):
    template_name='superuser/student_edit.html'
    model=Student
    form_class=StudentForm

    def get_success_url(self):
        return reverse('students:students_manage')


class SUStudentDelete(TeacherOwnedStudentMixin,DeleteView):
    template_name='superuser/student_delete.html'
    model=Student

    def get_success_url(self):
        return reverse('students:students_manage')


# ---------- Superuser-side grade management ----------

class SUGradeList(ListView):
    template_name='superuser/grades_manage.html'
    model=Grade
    context_object_name='grades'

    def get_queryset(self):
        return Grade.objects.all().order_by('id')


class SUGradeCreate(CreateView):
    template_name='superuser/grade_add.html'
    model=Grade
    form_class=GradeForm

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['page_title']='إضافة صف دراسي جديد'
        context['page_subtitle']='أدخل اسم الصف الدراسي لإضافته إلى النظام.'
        return context

    def get_success_url(self):
        return reverse('students:grade_manage')


class SUGradeUpdate(UpdateView):
    template_name='superuser/grade_add.html'
    model=Grade
    form_class=GradeForm

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['page_title']='تعديل الصف الدراسي'
        context['page_subtitle']='حدّث اسم الصف الدراسي ثم اضغط حفظ.'
        return context

    def get_success_url(self):
        return reverse('students:grade_manage')


class SUGradeDelete(DeleteView):
    template_name='superuser/grade_delete.html'
    model=Grade

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['students_count']=self.object.student_set.count()
        return context

    def post(self, request, *args, **kwargs):
        self.object=self.get_object()
        if self.object.student_set.exists():
            messages.error(request,'لا يمكن حذف صف مرتبط بتلاميذ !')
            return redirect('students:grade_delete_su', pk=self.object.pk)
        response=super().post(request,*args,**kwargs)
        messages.success(request,'تم حذف الصف الدراسي بنجاح')
        return response

    def get_success_url(self):
        return reverse('students:grade_manage')
