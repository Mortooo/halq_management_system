from datetime import date
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.db.models import Q
from django.views.decorators.http import require_POST

from halaqs.models import Halaqa
from students.models import Student
from attendances.models import TeachAttendance,StudAttendance
from django.views.generic import ListView,CreateView,UpdateView,DeleteView

from teachers.forms import TeacherForm
from halaqs.forms import HalaqaForm
from teachers.models import Teacher
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.

def dashboard(request):

    today_date=date.today()# get today date
    user=request.user.first_name # user is log in
    total_halaqats=Halaqa.objects.all().count()
    total_students=Student.objects.all().count()
    halaqats=Halaqa.objects.select_related('res_teacher').order_by('name')

    total_teachers=Teacher.objects.all().count()
    teachers_present_today=TeachAttendance.objects.filter(day=today_date,status=True).count()

    students_recorded_today=StudAttendance.objects.filter(day=today_date).count()
    students_present_today=StudAttendance.objects.filter(day=today_date,status=True).count()
    if students_recorded_today:
        avg_attendance=int(students_present_today*100/students_recorded_today)
    else:
        avg_attendance=0

    #################### add to context #####################
    context ={
        'today_date':today_date,
        'user' :user,
        'total_halaqats':total_halaqats,
        'total_students':total_students,
        'halaqats':halaqats,
        'teachers_present_today':teachers_present_today,
        'total_teachers':total_teachers,
        'avg_attendance':avg_attendance,
    }



    return render(request,'administration/dashboard.html',context)


class TeacherList(ListView):
    model=Teacher
    template_name='administration/teacher_manage.html'
    context_object_name='teachers'
    
    def get_queryset(self):
        query=super().get_queryset()
        
        if self.request.GET.get('q'):
            name=self.request.GET.get('q').rstrip()
            query=query.filter(name__icontains=name)
        
        
        
        
        return query

class TeacherCreate(CreateView):
    template_name='administration/teacher_add.html'
    model=Teacher
    form_class=TeacherForm
    success_url=reverse_lazy('administration:teacher_list')
    
class TeacherUpdate(UpdateView):
    template_name='administration/teacher_add.html'
    model=Teacher
    form_class=TeacherForm
    success_url=reverse_lazy('administration:teacher_list')
    
class TeacherDelete(DeleteView):
    template_name='administration/teacher_delete.html'
    model=Teacher
    success_url=reverse_lazy('administration:teacher_list')

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['has_account']=self.object.user_name_id is not None
        return context

    def post(self, request, *args, **kwargs):
        self.object=self.get_object()
        user=self.object.user_name
        response=super().post(request,*args,**kwargs)
        # teacher gone -> her login goes too (never destroy a superuser account)
        if user is not None and not user.is_superuser:
            user.delete()
        elif user is not None:
            messages.warning(request,'تم حذف المعلمة مع الإبقاء على حسابها لأنه حساب مدير !')
        else:
            messages.success(request,'تم حذف المعلمة بنجاح')
        return response
    

class HalaqaList(ListView):
    model=Halaqa
    template_name='administration/halaqa_manage.html'
    context_object_name='halaqats'

    def get_queryset(self):
        query=super().get_queryset()
        if self.request.GET.get('q'):
            name=self.request.GET.get('q').rstrip()
            query=query.filter(name__icontains=name)

        return query


class HalaqaCreate(CreateView):
    template_name='administration/halaqa_add.html'
    model=Halaqa
    form_class=HalaqaForm
    success_url=reverse_lazy('administration:halaqa_list')


class HalaqaUpdate(UpdateView):
    template_name='administration/halaqa_add.html'
    model=Halaqa
    form_class=HalaqaForm
    success_url=reverse_lazy('administration:halaqa_list')

class HalaqaDelete(DeleteView):
    template_name='administration/halaqa_delete.html'
    model=Halaqa
    context_object_name='halaqa'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        # weekly reports cascade-delete with the halaqa -> must be surfaced
        context['reports_count']=self.object.weekreport_set.count()
        context['students_count']=self.object.student_set.count()
        return context

    def post(self, request, *args, **kwargs):
        self.object=self.get_object()
        if self.object.weekreport_set.exists():
            messages.error(request,'لا يمكن حذف حلقة مرتبطة بتقارير أسبوعية !')
            return redirect('administration:delete_halaqa', pk=self.object.pk)
        response=super().post(request,*args,**kwargs)
        messages.success(request,'تم حذف الحلقة بنجاح')
        return response

    def get_success_url(self):
        return reverse('administration:halaqa_list')

class UsersList(ListView):
    template_name="administration/user_manage.html"
    model=User
    context_object_name='users'

    def get_queryset(self):
        query=super().get_queryset().prefetch_related('teacher').order_by('username')
        if self.request.GET.get('q'):
            q=self.request.GET.get('q').rstrip()
            query=query.filter(Q(username__icontains=q)|Q(first_name__icontains=q))
        return query


@require_POST
def toggle_user_active(request, pk):
    target=get_object_or_404(User, pk=pk)
    if target.is_superuser:
        messages.error(request,'لا يمكن تعطيل حساب المشرفة !')
        return redirect('administration:users_list')
    target.is_active=not target.is_active
    target.save()
    if target.is_active:
        messages.success(request,'تم تنشيط الحساب بنجاح')
    else:
        messages.success(request,'تم تعطيل الحساب ولن تستطيع الدخول')
    return redirect('administration:users_list')


class UserDelete(DeleteView):
    template_name='administration/user_delete.html'
    model=User
    context_object_name='target_user'

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['is_linked']=Teacher.objects.filter(user_name_id=self.object.pk).exists()
        return context

    def post(self, request, *args, **kwargs):
        self.object=self.get_object()
        if self.object.is_superuser:
            messages.error(request,'لا يمكن حذف حساب المشرفة !')
            return redirect('administration:users_list')
        if Teacher.objects.filter(user_name_id=self.object.pk).exists():
            messages.error(request,'هذا الحساب مرتبط بمعلمة ! احذفي المعلمة من إدارة المعلمات وسيُحذف الحساب معها.')
            return redirect('administration:delete_user', pk=self.object.pk)
        response=super().post(request,*args,**kwargs)
        messages.success(request,'تم حذف المستخدم بنجاح')
        return response

    def get_success_url(self):
        return reverse('administration:users_list')
