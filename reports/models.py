from django.db import models
from datetime import date
from halaqs.models import Halaqa

# Create your models here.
class WeekReport(models.Model):
    halaqa=models.ForeignKey(Halaqa,on_delete=models.CASCADE)
    end_w_date=models.DateField(default=date.today)
    amount=models.TextField(blank=False,null=False)
    compare_plan=models.CharField(max_length=10,blank=False,null=False)
    notes=models.TextField(blank=True,null=True)
    
    @property
    def teacher(self):
        teach=Halaqa.objects.get(pk=self.halaqa.id).res_teacher
        
        return teach
    
