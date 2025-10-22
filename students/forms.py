
from datetime import date
from django.forms import ModelForm
from django import forms
from .models import Student

class StudentForm(ModelForm):
    
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
            'name':forms.TextInput(attrs={'class':'w-full p-3 bg-slate-900 border border-slate-600 rounded-lg text-slate-200 focus:ring-2 focus:ring-blue-500'}),
            'address':forms.TextInput(attrs={'class':'w-full p-3 bg-slate-900 border border-slate-600 rounded-lg text-slate-200 focus:ring-2 focus:ring-blue-500'}),
            'tel':forms.TextInput(attrs={'class':'w-full p-3 bg-slate-900 border border-slate-600 rounded-lg text-slate-200 focus:ring-2 focus:ring-blue-500'}),
            'halaqa':forms.Select(attrs={'class':'w-full p-3 bg-slate-900 border border-slate-600 rounded-lg text-slate-200 focus:ring-2 focus:ring-blue-500'}),
            'status':forms.CheckboxInput(attrs={'class':"h-4 w-4 rounded bg-slate-700 border-slate-500 text-blue-600 focus:ring-blue-500"}),
            'date_birth':forms.DateInput(
                attrs={'class':'w-full p-3 bg-slate-900 border border-slate-600 rounded-lg text-slate-200 focus:ring-2 focus:ring-blue-500','type':'date'}),
            'add_course':forms.TextInput(attrs={'class':'w-full p-3 bg-slate-900 border border-slate-600 rounded-lg text-slate-200 focus:ring-2 focus:ring-blue-500'}),
            'grade':forms.Select(attrs={'class':'w-full p-3 bg-slate-900 border border-slate-600 rounded-lg text-slate-200 focus:ring-2 focus:ring-blue-500'})         
        }
        
        
    def clean(self):
        clean_data=super().clean()
        name=clean_data.get('name')
        d_birth=clean_data.get('date_birth')
        
        # two students cannot have the same name 
        if not self.instance.pk:
            if Student.objects.filter(name=name).exists():
                raise forms.ValidationError('يوجد طالب في قاعدة البيانات يحمل نفس الإسم !  ')
            
        # vaildting date 
        if d_birth:
            if d_birth >= date.today():
                raise forms.ValidationError('تاريخ الميلاد يجب أن لا يكون في المستقبل أو اليوم !')
            elif (date.today().year - d_birth.year) < 1 :
                raise forms.ValidationError('يجب أن لا يقل عمر التلميذ عن سنة !')

        
        
        return clean_data
        