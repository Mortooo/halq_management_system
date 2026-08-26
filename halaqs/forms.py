from django import forms
from .models import Halaqa
from teachers.models import Teacher

INPUT_CLASS = 'input'

class HalaqaForm(forms.ModelForm):

    class Meta:
        model = Halaqa
        fields = ['name', 'res_teacher', 'course', 'notes']

        labels = {
            'name': 'اسم الحلقة :',
            'res_teacher': 'المعلمة المسؤولة :',
            'course': 'المقرر :',
            'notes': 'ملاحظات :',
        }

        widgets = {
            'name': forms.TextInput(attrs={'class': INPUT_CLASS}),
            'res_teacher': forms.Select(attrs={'class': INPUT_CLASS}),
            'course': forms.TextInput(attrs={'class': INPUT_CLASS}),
            'notes': forms.Textarea(attrs={'class': INPUT_CLASS + ' h-24', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        self.school = kwargs.pop('school', None)
        super().__init__(*args, **kwargs)
        if self.school:
            self.fields['res_teacher'].queryset = Teacher.objects.filter(school=self.school)

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if name:
            qs = Halaqa.objects.filter(name__iexact=name)
            if self.school:
                qs = qs.filter(school=self.school)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError('يوجد حلقة في قاعدة البيانات بنفس الاسم !')
        return name
