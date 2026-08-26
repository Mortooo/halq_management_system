from datetime import date
from django.shortcuts import redirect, render
from django.views.generic import ListView
from django.db.models import OuterRef, Subquery

from halaqs.models import Halaqa
from students.models import Student
from teachers.models import Teacher
from .models import StudAttendance,TeachAttendance
from django.contrib import messages


def _to_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _parse_range(start_value, end_value):
    if not start_value or not end_value:
        return None
    try:
        start=date.fromisoformat(start_value)
        end=date.fromisoformat(end_value)
    except ValueError:
        return None
    if start > end:
        return None
    return (start, end)


class StudentAttList(ListView):
    template_name='attendances/student_att.html'
    model=Student
    context_object_name='students_att'


    def get_queryset(self):
        today=date.today()
        user=self.request.user
        queryset=Student.objects.filter(halaqa__res_teacher__user_name=user,status=True,school=self.request.school)

        selected_halaqa=_to_int(self.request.GET.get("selected_halaqa"))
        if selected_halaqa:
            queryset=queryset.filter(halaqa__id=selected_halaqa)

        att_today=Subquery(
            StudAttendance.objects.filter(student=OuterRef('pk'),day=today).values('status')[:1]
        )
        notes_today=Subquery(
            StudAttendance.objects.filter(student=OuterRef('pk'),day=today).values('notes')[:1]
        )
        att_id=Subquery(
            StudAttendance.objects.filter(student=OuterRef('pk'),day=today).values('id')[:1]
        )
        queryset=queryset.annotate(
            att_status=att_today, att_notes=notes_today, att_id=att_id
        ).order_by('halaqa__name','name')

        return queryset

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        user=self.request.user
        halaqats=Halaqa.objects.filter(res_teacher__user_name=user,school=self.request.school).order_by('name')
        context['halaqats']=halaqats
        context['today_date']=date.today()
        return context


    def post(self,request,*args, **kwargs):
        today=date.today()
        student_ids = request.POST.getlist('student_id')
        saved=0

        for student_id in student_ids:
            student=Student.objects.filter(id=student_id,halaqa__res_teacher__user_name=request.user,school=request.school).first()
            if student is None:
                continue
            status=request.POST.get(f'status_{student_id}')=='True'
            notes=request.POST.get(f'notes_{student_id}')

            StudAttendance.objects.update_or_create(
                student=student,
                day=today,
                defaults={
                'status': status,
                'notes': notes
                }
            )
            saved+=1

        if saved:
            messages.success(request, f"تم حفظ سجلات حضور {saved} تلميذ/ة بنجاح")
        else:
            messages.warning(request, "لم يتم حفظ أي سجل !")

        return redirect(request.get_full_path())

class TeacherAttList(ListView):
    template_name='attendances/teacher_attendance.html'
    model=Teacher
    context_object_name='teacher_att'


    def get_queryset(self):
        today=date.today()
        queryset=Teacher.objects.filter(school=self.request.school)

        att_today=Subquery(
            TeachAttendance.objects.filter(teacher=OuterRef('pk'),day=today).values('status')[:1]
        )
        notes_today=Subquery(
            TeachAttendance.objects.filter(teacher=OuterRef('pk'),day=today).values('notes')[:1]
        )
        queryset=queryset.annotate(
            att_status=att_today, att_notes=notes_today
        ).order_by('name')

        return queryset


    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['today_date']=date.today()
        return context


    def post(self,request,*args, **kwargs):
        today=date.today()
        teacher_ids = request.POST.getlist('teacher_id')
        saved=0

        for teacher_id in teacher_ids:
            teacher=Teacher.objects.filter(id=teacher_id,school=request.school).first()
            if teacher is None:
                continue
            status=request.POST.get(f'status_{teacher_id}')=='True'
            notes=request.POST.get(f'notes_{teacher_id}')

            TeachAttendance.objects.update_or_create(
                teacher=teacher,
                day=today,
                defaults={
                'status': status,
                'notes': notes
                }
            )
            saved+=1

        if saved:
            messages.success(request, f"تم حفظ سجلات حضور {saved} معلمة/ة بنجاح")
        else:
            messages.warning(request, "لم يتم حفظ أي سجل !")

        return redirect(request.get_full_path())


class AttendanceRecord(ListView):
    template_name='attendances/attendance_record.html'
    model=TeachAttendance
    context_object_name='teacher_att'
    paginate_by=30

    def get_queryset(self):
        queryset=super().get_queryset().select_related('teacher').filter(teacher__school=self.request.school)

        teacher_id=_to_int(self.request.GET.get('teacher'))
        range_dates=_parse_range(self.request.GET.get('start_date'),self.request.GET.get('end_date'))

        if teacher_id:
            queryset=queryset.filter(teacher_id=teacher_id)
        if range_dates:
            queryset=queryset.filter(day__range=range_dates)

        return queryset.order_by('-day','teacher__name')


    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['teachers']=Teacher.objects.filter(school=self.request.school).order_by('name')
        return context


class StudentRecord(ListView):
    template_name='attendances/student_record.html'
    model=StudAttendance
    context_object_name='students_records'
    paginate_by=30

    def get_queryset(self):
        queryset=super().get_queryset().select_related('student','student__halaqa').filter(student__school=self.request.school)

        halaqa_id=_to_int(self.request.GET.get('halaqa'))
        range_dates=_parse_range(self.request.GET.get('start_date'),self.request.GET.get('end_date'))

        if halaqa_id:
            queryset=queryset.filter(student__halaqa_id=halaqa_id)
        if range_dates:
            queryset=queryset.filter(day__range=range_dates)

        return queryset.order_by('-day','student__name')


    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['halaqats']=Halaqa.objects.filter(school=self.request.school).select_related('res_teacher').order_by('name')
        return context
