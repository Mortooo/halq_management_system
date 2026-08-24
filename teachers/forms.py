from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.db import transaction
from .models import Teacher

INPUT_CLASS = 'w-full p-3 bg-slate-900 border border-slate-600 rounded-lg text-slate-200 focus:ring-2 focus:ring-blue-500'


def validate_tel(value):
    if not value.isdigit() or not (9 <= len(value) <= 10):
        raise forms.ValidationError('رقم الهاتف يجب أن يحتوي على أرقام فقط (9-10 خانات).')


class TeacherForm(ModelForm):

    tel = forms.CharField(
        max_length=10,
        validators=[validate_tel],
        required=False,
    )

    username = forms.CharField(
        max_length=150,
        label='اسم المستخدم :',
        widget=forms.TextInput(attrs={'class': INPUT_CLASS, 'autocomplete': 'off'}),
    )

    password = forms.CharField(
        label='كلمة المرور :',
        widget=forms.PasswordInput(attrs={'class': INPUT_CLASS, 'autocomplete': 'new-password'}),
        required=False,
        strip=False,
    )

    field_order = ['name', 'tel', 'address', 'email', 'username', 'password']

    class Meta:
        model = Teacher

        fields = ['name', 'tel', 'address', 'email']
        labels = {
            'name': 'اسم المعلمة :',
            'address': 'عنوان السكن : ',
            'tel': 'رقم الهاتف : ',
            'email': 'البريد الالكتروني :',
        }

        widgets = {
            'name': forms.TextInput(attrs={'class': INPUT_CLASS}),
            'address': forms.TextInput(attrs={'class': INPUT_CLASS}),
            'tel': forms.TextInput(attrs={'class': INPUT_CLASS}),
            'email': forms.EmailInput(attrs={'class': INPUT_CLASS}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        has_account = bool(self.instance.pk and self.instance.user_name_id)
        if has_account:
            self.fields['password'].required = False
            self.fields['password'].label = 'كلمة مرور جديدة :'
            self.fields['username'].initial = self.instance.user_name.username
        else:
            self.fields['password'].required = True
            self.fields['password'].label = 'كلمة المرور :'

    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip()
        if username:
            qs = User.objects.filter(username__iexact=username)
            if self.instance.user_name_id:
                qs = qs.exclude(pk=self.instance.user_name_id)
            if qs.exists():
                raise forms.ValidationError('اسم المستخدم مستخدم بالفعل !')
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password') or ''
        if not password:
            return password
        if len(password) < 8:
            raise forms.ValidationError('كلمة المرور يجب أن تكون 8 خانات على الأقل !')
        if password.isdigit():
            raise forms.ValidationError('كلمة المرور لا يمكن أن تحتوي على أرقام فقط !')
        if password == self.cleaned_data.get('username'):
            raise forms.ValidationError('كلمة المرور لا يمكن أن تكون مطابقة لاسم المستخدم !')
        return password

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if name:
            qs = Teacher.objects.filter(name__icontains=name)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError('يوجد معلمة في قاعدة البيانات تحمل نفس الاسم !')
        return name

    def save(self, commit=True):
        teacher = super().save(commit=False)
        with transaction.atomic():
            user = self.instance.user_name
            new_password = self.cleaned_data.get('password') or ''
            if user is None:
                user = User(
                    username=self.cleaned_data['username'],
                    email=teacher.email or '',
                    first_name=teacher.name,
                    is_staff=True,
                )
                user.set_password(new_password)
                user.save()
            else:
                user.username = self.cleaned_data['username']
                user.first_name = teacher.name
                user.email = teacher.email or ''
                if new_password:
                    user.set_password(new_password)
                user.save()
            teacher.user_name = user
            teacher.save()
        return teacher
