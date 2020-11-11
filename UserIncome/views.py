from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Source,Income
from django.contrib import messages 
from django.core.paginator import Paginator
import datetime
from django.http import JsonResponse
from django.http import JsonResponse,HttpResponse
from django.template.loader import render_to_string
import tempfile
from django.db.models import Sum
from weasyprint import HTML
# Create your views here.
#this is home route after login 
@login_required(login_url='/authentication/login')
def home(requests):
    income=Income.objects.filter(owner=requests.user)
    paginator=Paginator(income,4)
    page_number=requests.GET.get('page')
    page_obj=Paginator.get_page(paginator,page_number)
    context={'income':income,'page_obj':page_obj}
    return render(requests,'Income/index.html',context)

# you can add your income using this function
def Add_Income(requests):
    if requests.method=='GET':
        source=Source.objects.all()
        context={'source':source}
        return render(requests,'Income/add_income.html',context) 
    if requests.method=='POST':
        amount=requests.POST['amount']
        date=requests.POST['date']  
        description=requests.POST['description'] 
        source=requests.POST['source'] 
        Income.objects.create(amount=amount,date=date,description=description,source=source,owner=requests.user) 
        messages.success(requests,'Successfully income added')
        return redirect('income') 

#you can add your edit income using this function
def Edit_Income(requests,id):
    income=Income.objects.get(pk=id)
    source=Source.objects.all()
    context={'source':source,
            'income':income
           }
    if requests.method=='GET':
        return render(requests,'Income/edit_income.html',context)
    else:
        amount=requests.POST['amount']
        date=requests.POST['date']  
        description=requests.POST['description'] 
        source=requests.POST['source'] 
        income.amount=amount
        income.date=date
        income.description=description
        income.source=source
        income.owner=requests.user
        income.save()
        messages.info(requests,'Successfully updated') 
        return redirect('income') 
#y delete a particular row using this function
def Delete_Income(requests,id):
    income=Income.objects.get(pk=id)
    income.delete()
    messages.success(requests,'Successfully Deleted') 
    return redirect('income')

#search  income data  through source 
def Search(requests):
    page_number=requests.GET.get('page')
         
    query=requests.POST['search']
    income = Income.objects.filter(source__icontains=query)
    paginator=Paginator(income,4)
         
    page_obj=Paginator.get_page(paginator,page_number)
    if income:
        context={'income':income,'page_obj':page_obj}
    else:
        context={'income':income,'page_obj':page_obj,'search':'fgty'}    

         
     
    
    return render(requests,'Income/index.html',context)

#income summary
def income_category_summary(requests):
    today_date=datetime.date.today()
    six_month_ago = today_date-datetime.timedelta(days=30*6)
    income= Income.objects.filter(owner=requests.user,
        date__gte=six_month_ago,date__lte=today_date
    )
    finalrep={}
    def get_source(income):
        return income.source
    source_list=list(set(map(get_source,income))) 
    def get_income_source_amount(source):
        amount=0
        filter_by_source=income.filter(source=source)
        for item in filter_by_source:
            amount+=item.amount

        return amount

    for x in income:
        for y in source_list:
            finalrep[y] = get_income_source_amount(y)  
    return  JsonResponse({'income_category':finalrep})          

def statsView(request):
    return render(request,'expense/stats1.html')      

# generate output pdf
def export_pdf(requests):
    response=HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=Income' + \
        str(datetime.datetime.now()) +'.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    income=Income.objects.filter(owner=requests.user)
    sum=income.aggregate(Sum('amount'))
    html_string=render_to_string(
        'Income/pdf-output.html',{'income':income,'total':sum['amount__sum']}
    )  
    html=HTML(string=html_string)  
    result=html.write_pdf()

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name,'rb')
        response.write(output.read())
    return response   
