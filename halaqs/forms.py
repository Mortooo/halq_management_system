from django import forms
from .models import Halaqa

INPUT_CLASS = 'w-full p-3 bg-slate-900 border border-slate-600 rounded-lg text-slate-200 focus:ring-2 focus:ring-blue-500'

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
