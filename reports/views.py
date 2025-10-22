from datetime import date, timedelta
from django.shortcuts import render

from halaqs.models import Halaqa
from reports.models import WeekReport
from teachers.models import Teacher

# Create your views here.

def show_weekly_report(request,pk):

    # Get the date of the end of week 
    today = date.today()
    week_end_day = 3
    days_until_thursday = week_end_day - today.weekday()
    if days_until_thursday < 0:
        days_until_thursday += 7

    end_of_week = today + timedelta(days=days_until_thursday)
    #list of halaqats that teacher responsable of 
    user=request.user
    teacher=Teacher.objects.get(user_name=user)
    halaqats=Halaqa.objects.filter(res_teacher=teacher.id)
    #####################################################################
       
    if request.method == 'GET' :
                        
        context={'current_week_end_date':end_of_week,'halaqats':halaqats,}
        
        return render(request,'weekly_report.html',context)
    
    if request.method == 'POST': 
        
        halaqa=request.POST.get('halaqa')
        progress=request.POST.get('progress')
        plan_status=request.POST.get('plan_status')
        delay_reason=request.POST.get('delay_reason')
        advanced_amount=request.POST.get('advanced_reason')
        notes=''
        
        if plan_status=='advanced':
            notes=advanced_amount
        elif plan_status=='delayed':
            notes=delay_reason
        
        selected_halaqa = Halaqa.objects.get(id=halaqa)
        
        #check if there are reprort of this halaqa in this week if yes update if no create 
        if WeekReport.objects.filter(end_w_date=end_of_week,halaqa=selected_halaqa).exists():
            
             WeekReport.objects.filter(end_w_date=end_of_week,halaqa=selected_halaqa).update(
                halaqa=selected_halaqa,
                amount=progress,
                compare_plan=plan_status,
                notes=notes,
                end_w_date=end_of_week
            )
        else:
            WeekReport.objects.create(
                halaqa=selected_halaqa,
                amount=progress,
                compare_plan=plan_status,
                notes=notes,
                end_w_date=end_of_week

            )
        
        context={'current_week_end_date':end_of_week,'halaqats':halaqats,}
        
        return render(request,'weekly_report.html',context)
    
    
