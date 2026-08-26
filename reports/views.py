from datetime import date, timedelta

from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView

from halaqs.models import Halaqa
from reports.models import WeekReport
from teachers.models import Teacher


def _to_int(value):
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return None


def _week_end_date():
    today = date.today()
    days_until_thursday = 3 - today.weekday()
    if days_until_thursday < 0:
        days_until_thursday += 7
    return today + timedelta(days=days_until_thursday)


def show_weekly_report(request):
    end_of_week = _week_end_date()
    school = request.school

    teacher = Teacher.objects.filter(user_name=request.user,school=school).first() if request.user.is_authenticated else None
    halaqats = Halaqa.objects.filter(res_teacher=teacher,school=school) if teacher else Halaqa.objects.none()

    if request.method == 'GET':
        return render(request, 'reports/weekly_report.html',
                      {'current_week_end_date': end_of_week, 'halaqats': halaqats})

    progress = request.POST.get('progress', '').strip()
    plan_status = request.POST.get('plan_status')

    notes = ''
    if plan_status == 'advanced':
        notes = request.POST.get('advanced_reason', '').strip()
    elif plan_status == 'delayed':
        notes = request.POST.get('delay_reason', '').strip()

    if request.user.is_superuser:
        selected_halaqa = Halaqa.objects.filter(id=_to_int(request.POST.get('halaqa')),school=school).first()
    else:
        selected_halaqa = halaqats.filter(id=_to_int(request.POST.get('halaqa'))).first()

    if selected_halaqa is None or not progress or plan_status not in ('on_track', 'advanced', 'delayed'):
        messages.error(request, 'يرجى اختيار الحلقة وكتابة مقدار المنجز بشكل صحيح.')
        return render(request, 'reports/weekly_report.html',
                      {'current_week_end_date': end_of_week, 'halaqats': halaqats})

    WeekReport.objects.update_or_create(
        halaqa=selected_halaqa,
        end_w_date=end_of_week,
        defaults={'amount': progress, 'compare_plan': plan_status, 'notes': notes},
    )
    messages.success(request, 'تم إرسال التقرير الأسبوعي بنجاح.')

    return redirect('reports:weekly_report')


class TotalReport(ListView):
    template_name = 'reports/total_reports.html'
    model = WeekReport
    context_object_name = 'reports_list'
    paginate_by = 30

    def get_queryset(self):
        qs = super().get_queryset().select_related('halaqa__res_teacher').filter(halaqa__school=self.request.school).order_by('-end_w_date', 'halaqa__name')

        teacher = _to_int(self.request.GET.get('teacher'))
        if teacher:
            qs = qs.filter(halaqa__res_teacher_id=teacher)

        halaqa = _to_int(self.request.GET.get('halaqa'))
        if halaqa:
            qs = qs.filter(halaqa_id=halaqa)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['halaqats_list'] = Halaqa.objects.filter(school=self.request.school).order_by('name')
        context['teachers'] = Teacher.objects.filter(school=self.request.school).order_by('name')
        return context


class ReportDetails(DetailView):
    template_name = 'reports/report_details.html'
    model = WeekReport
    context_object_name = 'report'
