from datetime import date
from django.forms import ModelForm
from django import forms
from .models import Student, Grade
from halaqs.models import Halaqa

INPUT_CLASS = 'input'


def validate_tel(value):
    if not value.isdigit() or not (9 <= len(value) <= 10):
        raise forms.ValidationError('رقم الهاتف يجب أن يحتوي على أرقام فقط (9-10 خانات).')


class StudentForm(ModelForm):

    tel = forms.CharField(
        max_length=10,
        validators=[validate_tel],
        widget=forms.TelInput(attrs={'class': INPUT_CLASS, 'placeholder': '05XXXXXXXX', 'dir': 'ltr', 'style': 'text-align:left'}),
    )

    class Meta:
        model=Student
        fields=['name','address','tel','halaqa','status','date_birth','add_course','grade']

        labels={
            'name':'الاسم كامل :',
            'address':'عنوان السكن :',
            'tel':'رقم الهاتف :',
            'halaqa':'الحلقة :',
            'status':'حالة الطالب :',
            'date_birth':'تاريخ الميلاد :',
            'add_course':'المقرر الاضافي :',
            'grade':'الصف الدراسي : '
        }

        widgets={
            'name':forms.TextInput(attrs={'class':INPUT_CLASS}),
            'address':forms.TextInput(attrs={'class':INPUT_CLASS}),
            'tel':forms.TelInput(attrs={'class':INPUT_CLASS, 'placeholder': '05XXXXXXXX', 'dir': 'ltr', 'style': 'text-align:left'}),
            'halaqa':forms.Select(attrs={'class':INPUT_CLASS}),
            'status':forms.CheckboxInput(attrs={'class':"h-4 w-4 rounded bg-slate-700 border-slate-500 text-blue-600 focus:ring-blue-500"}),
            'date_birth':forms.DateInput(
                attrs={'class':INPUT_CLASS,'type':'date'}),
            'add_course':forms.TextInput(attrs={'class':INPUT_CLASS}),
            'grade':forms.Select(attrs={'class':INPUT_CLASS})
        }


    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        # teachers may only place students in their own halaqat
        if user is not None and not user.is_superuser:
            self.fields['halaqa'].queryset = Halaqa.objects.filter(res_teacher__user_name=user)


    def clean(self):
        clean_data=super().clean()
        name=clean_data.get('name')
        d_birth=clean_data.get('date_birth')

        # two students cannot share the same name (case-insensitive, on create and update)
        if name:
            qs = Student.objects.filter(name__icontains=name)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError('يوجد طالب في قاعدة البيانات يحمل نفس الإسم !  ')

        # validating date (month/day aware age check)
        if d_birth:
            today=date.today()
            if d_birth >= today:
                raise forms.ValidationError('تاريخ الميلاد يجب أن لا يكون في المستقبل أو اليوم !')
            age = today.year - d_birth.year - ((today.month, today.day) < (d_birth.month, d_birth.day))
            if age < 1:
                raise forms.ValidationError('يجب أن لا يقل عمر التلميذ عن سنة !')

        return clean_data


class GradeForm(ModelForm):

    class Meta:
        model = Grade
        fields = ['name']
        labels = {'name': 'اسم الصف الدراسي :'}
        widgets = {'name': forms.TextInput(attrs={'class': INPUT_CLASS})}

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if name:
            qs = Grade.objects.filter(name__icontains=name)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError('يوجد صف دراسي بنفس الاسم !')
        return name
