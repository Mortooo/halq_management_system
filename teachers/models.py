from django.db import models
from halaqs.models import Halaqa
from django.contrib.auth.models import User

# Create your models here.
class Teacher(models.Model):
    name=models.CharField(max_length=100,blank=False,null=False)
    tel=models.CharField(max_length=10,blank=True,null=True)
    email=models.EmailField()
    address=models.CharField(max_length=100,blank=True,null=True)
    user_name=models.OneToOneField(User,on_delete=models.SET_NULL,blank=True,null=True)
    # res_halaqa=models.OneToOneField('halaqs.Halaqa',on_delete=models.SET_NULL,blank=True,null=True)
    
    def __str__(self):
        return self.name
    
