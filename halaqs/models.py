from django.db import models
from django import forms

# Create your models here.

class Halaqa(models.Model):
    name =models.CharField(max_length=50,blank=False,null=False)
    res_teacher=models.ForeignKey('teachers.Teacher',on_delete=models.SET_NULL,null=True,blank=True)
    course=models.CharField(max_length=50,blank=False,null=False)
    notes=models.TextField(blank=True,null=True)
    
    def __str__(self):
        return self.name