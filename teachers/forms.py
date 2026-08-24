from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
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

    class Meta:
        model = Teacher

        fields = ['name', 'tel', 'address', 'email', 'user_name']
        labels = {
            'name': 'اسم المعلمة :',
            'address': 'عنوان السكن : ',
            'tel': 'رقم الهاتف : ',
            'email': 'البريد الالكتروني :',
            'user_name': 'اسم المستخدم :'
        }

        widgets = {
            'name': forms.TextInput(attrs={'class': INPUT_CLASS}),
            'address': forms.TextInput(attrs={'class': INPUT_CLASS}),
            'tel': forms.TextInput(attrs={'class': INPUT_CLASS}),
            'email': forms.EmailInput(attrs={'class': INPUT_CLASS}),
            'user_name': forms.Select(attrs={'class': INPUT_CLASS})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # only offer users not already linked to another teacher
        taken = Teacher.objects.exclude(user_name=None)
        if self.instance.pk:
            taken = taken.exclude(pk=self.instance.pk)
        used_ids = list(taken.values_list('user_name_id', flat=True))
        self.fields['user_name'].queryset = User.objects.exclude(id__in=used_ids)
        self.fields['user_name'].error_messages['invalid_choice'] = 'هذا المستخدم مرتبط بمعلمة أخرى !'

    def clean_user_name(self):
        user = self.cleaned_data.get('user_name')
        if user:
            qs = Teacher.objects.filter(user_name=user)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError('هذا المستخدم مرتبط بمعلمة أخرى !')
        return user

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if name:
            qs = Teacher.objects.filter(name__icontains=name)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError('يوجد معلمة في قاعدة البيانات تحمل نفس الاسم !')
        return name
