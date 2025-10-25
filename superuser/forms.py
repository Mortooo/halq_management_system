
from django import forms
from django.forms import ModelForm

from teachers.models import Teacher

class TeacherForm(ModelForm):
    
    class Meta:
        model=Teacher
        
        fields=['name','tel','address','email','user_name']
        labels={
            'name':'اسم المعلمة :',
            'address':'عنوان السكن : ',
            'tel':'رقم الهاتف : ',
            'email':'البريد الالكتروني :',
            'user_name':' اسم المسخدم :'   
        }
        
        widgets={
            'name':forms.TextInput(attrs={'class':'w-full p-3 bg-slate-900 border border-slate-600 rounded-lg text-slate-200 focus:ring-2 focus:ring-blue-500'}),
            'address':forms.TextInput(attrs={'class':'w-full p-3 bg-slate-900 border border-slate-600 rounded-lg text-slate-200 focus:ring-2 focus:ring-blue-500'}),
            'tel':forms.TextInput(attrs={'class':'w-full p-3 bg-slate-900 border border-slate-600 rounded-lg text-slate-200 focus:ring-2 focus:ring-blue-500'}),
            'email':forms.EmailInput(attrs={'class':'w-full p-3 bg-slate-900 border border-slate-600 rounded-lg text-slate-200 focus:ring-2 focus:ring-blue-500'}),
            'user_name':forms.CheckboxInput(attrs={'class':"h-4 w-4 rounded bg-slate-700 border-slate-500 text-blue-600 focus:ring-blue-500"}),
            'user_name':forms.Select(attrs={'class':'w-full p-3 bg-slate-900 border border-slate-600 rounded-lg text-slate-200 focus:ring-2 focus:ring-blue-500'})         
        }
        
        
      
    