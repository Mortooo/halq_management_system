from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django import forms
from .models import School, UserProfile
from django.db.models import Count
from datetime import date

DEFAULT_GRADES = [
    'الصف الأول الابتدائي',
    'الصف الثاني الابتدائي',
    'الصف الثالث الابتدائي',
    'الصف الرابع الابتدائي',
    'الصف الخامس الابتدائي',
    'الصف السادس الابتدائي',
    'الصف الأول المتوسط',
    'الصف الثاني المتوسط',
    'الصف الثالث المتوسط',
    'الصف الأول الثانوي',
    'الصف الثاني الثانوي',
    'الصف الثالث الثانوي',
]


def create_default_grades(school):
    from students.models import Grade
    for name in DEFAULT_GRADES:
        Grade.objects.get_or_create(name=name, school=school)


class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ['name', 'address', 'tel', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input', 'placeholder': 'اسم المدرسة'}),
            'address': forms.TextInput(attrs={'class': 'input', 'placeholder': 'العنوان'}),
            'tel': forms.TextInput(attrs={'class': 'input', 'type': 'tel', 'placeholder': '05XXXXXXXX'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'h-5 w-5 text-emerald-600 rounded'}),
        }


class RegisterSchoolForm(forms.Form):
    school_name = forms.CharField(
        max_length=100,
        label='اسم المدرسة',
        widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'اسم المدرسة أو الحلقة'}),
    )
    school_address = forms.CharField(
        max_length=200,
        required=False,
        label='العنوان',
        widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'العنوان (اختياري)'}),
    )
    school_tel = forms.CharField(
        max_length=15,
        required=False,
        label='هاتف المدرسة',
        widget=forms.TextInput(attrs={'class': 'input', 'type': 'tel', 'placeholder': '05XXXXXXXX'}),
    )
    username = forms.CharField(
        max_length=150,
        label='اسم المستخدم',
        widget=forms.TextInput(attrs={'class': 'input', 'placeholder': 'اسم المستخدم للدخول'}),
    )
    email = forms.EmailField(
        label='البريد الإلكتروني',
        widget=forms.EmailInput(attrs={'class': 'input', 'placeholder': 'email@example.com'}),
    )
    password1 = forms.CharField(
        label='كلمة المرور',
        widget=forms.PasswordInput(attrs={'class': 'input', 'placeholder': 'كلمة المرور'}),
    )
    password2 = forms.CharField(
        label='تأكيد كلمة المرور',
        widget=forms.PasswordInput(attrs={'class': 'input', 'placeholder': 'أعد إدخال كلمة المرور'}),
    )

    def clean_school_name(self):
        school_name = self.cleaned_data.get('school_name', '').strip()
        if School.objects.filter(name=school_name).exists():
            raise forms.ValidationError('اسم المدرسة مستخدم بالفعل. يرجى اختيار اسم آخر.')
        return school_name

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('اسم المستخدم مستخدم بالفعل.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('البريد الإلكتروني مستخدم بالفعل.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password1')
        p2 = cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('كلمتا المرور غير متطابقتين.')
        return cleaned_data


class RegisterSchoolView(FormView):
    template_name = 'schools/register_school.html'
    form_class = RegisterSchoolForm
    success_url = reverse_lazy('administration:dashboard')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        d = form.cleaned_data
        with transaction.atomic():
            school = School.objects.create(
                name=d['school_name'],
                address=d.get('school_address', ''),
                tel=d.get('school_tel', ''),
                is_active=True,
            )
            user = User.objects.create_superuser(
                username=d['username'],
                email=d['email'],
                password=d['password1'],
            )
            UserProfile.objects.create(user=user, school=school)
            create_default_grades(school)

        try:
            login_url = self.request.build_absolute_uri(reverse_lazy('account_login'))
            html_message = render_to_string('schools/welcome_email.html', {
                'username': d['username'],
                'school_name': d['school_name'],
                'login_url': login_url,
                'year': date.today().year,
            })
            plain_message = strip_tags(html_message)
            send_mail(
                subject=f'مرحباً بك في نظام إدارة الحلقات - {d["school_name"]}',
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[d['email']],
                html_message=html_message,
                fail_silently=True,
            )
        except Exception:
            pass

        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        messages.success(self.request, f'تم إنشاء مدرسة "{school.name}" وحساب المدير بنجاح.')
        return super().form_valid(form)


class GlobalSchoolRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_superuser:
            from django.contrib.auth.views import redirect_to_login
            return redirect_to_login(request.get_full_path())
        if request.school is not None:
            from django.http import Http404
            raise Http404()
        return super().dispatch(request, *args, **kwargs)


class SchoolListView(GlobalSchoolRequiredMixin, ListView):
    model = School
    template_name = 'schools/school_list.html'
    context_object_name = 'schools'
    ordering = ['name']

    def get_queryset(self):
        return super().get_queryset().annotate(
            teacher_count=Count('teacher', distinct=True),
            student_count=Count('student', distinct=True),
            halaqa_count=Count('halaqa', distinct=True),
        )


class SchoolCreateView(GlobalSchoolRequiredMixin, CreateView):
    model = School
    template_name = 'schools/school_form.html'
    form_class = SchoolForm
    success_url = reverse_lazy('schools:school_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        create_default_grades(self.object)
        messages.success(self.request, 'تم إنشاء المدرسة بنجاح.')
        return response


class SchoolUpdateView(GlobalSchoolRequiredMixin, UpdateView):
    model = School
    template_name = 'schools/school_form.html'
    form_class = SchoolForm
    success_url = reverse_lazy('schools:school_list')

    def form_valid(self, form):
        messages.success(self.request, 'تم تحديث بيانات المدرسة بنجاح.')
        return super().form_valid(form)


class SchoolDeleteView(GlobalSchoolRequiredMixin, DeleteView):
    model = School
    template_name = 'schools/school_confirm_delete.html'
    success_url = reverse_lazy('schools:school_list')

    def form_valid(self, form):
        messages.success(self.request, 'تم حذف المدرسة بنجاح.')
        return super().form_valid(form)


class AssignSchoolUserView(GlobalSchoolRequiredMixin, View):
    def get(self, request, school_id):
        school = get_object_or_404(School, pk=school_id)
        users = User.objects.filter(profile__school=school).order_by('username')
        available = User.objects.filter(is_superuser=True).exclude(id__in=users.values_list('id', flat=True))
        return render(request, 'schools/school_users.html', {
            'school': school,
            'users': users,
            'available_users': available,
        })

    def post(self, request, school_id):
        school = get_object_or_404(School, pk=school_id)
        user_id = request.POST.get('user_id')
        action = request.POST.get('action')
        if action == 'add' and user_id:
            user = get_object_or_404(User, pk=user_id)
            UserProfile.objects.get_or_create(user=user, defaults={'school': school})
            messages.success(request, f'تم تعيين {user.username} إلى {school.name}.')
        elif action == 'remove' and user_id:
            UserProfile.objects.filter(user_id=user_id, school=school).delete()
            messages.success(request, 'تم إزالة المستخدم من المدرسة.')
        return redirect('schools:school_users', school_id=school.id)
