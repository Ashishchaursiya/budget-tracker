from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Category,Expense
from django.contrib import messages 
from django.core.paginator import Paginator
import datetime
from django.http import JsonResponse,HttpResponse
from django.template.loader import render_to_string
import tempfile
from django.db.models import Sum
from weasyprint import HTML


# Create your views here.
def index(requests):
    return render(requests,'expense/home.html')


# expens home page
@login_required(login_url='/authentication/login')
def home(requests):
    expense=Expense.objects.filter(owner=requests.user)
    paginator=Paginator(expense,4)
    page_number=requests.GET.get('page')
    page_obj=Paginator.get_page(paginator,page_number)
    context={'expens':expense,'page_obj':page_obj}
    return render(requests,'expense/index.html',context)

#add expense
def Add_Expense(requests):
    if requests.method=='GET':
        categories=Category.objects.all()
        context={'categories':categories}
        return render(requests,'expense/add_expense.html',context) 
    if requests.method=='POST':
        amount=requests.POST['amount']
        date=requests.POST['date']  
        description=requests.POST['description'] 
        category=requests.POST['category'] 
        Expense.objects.create(amount=amount,date=date,description=description,category=category,owner=requests.user) 
        messages.success(requests,'Successfully expense added')
        return redirect('expense') 

#edit expense    
def Edit_Expense(requests,id):
    expense=Expense.objects.get(pk=id)
    categories=Category.objects.all()
    context={'categories':categories,
            'expense':expense
           }
    if requests.method=='GET':
        return render(requests,'expense/edit_expense.html',context)
    else:
        amount=requests.POST['amount']
        date=requests.POST['date']  
        description=requests.POST['description'] 
        category=requests.POST['category'] 
        expense.amount=amount
        expense.date=date
        expense.description=description
        expense.category=category
        expense.owner=requests.user
        expense.save()
        messages.info(requests,'Successfully updated') 
        return redirect('expense') 

    #delete expense
def Delete_Expense(requests,id):
    expense=Expense.objects.get(pk=id)
    expense.delete()
    messages.success(requests,'Successfully Deleted') 
    return redirect('expense')



#find category of expense

def expense_category_summary(requests):
    today_date=datetime.date.today()
    six_month_ago = today_date-datetime.timedelta(days=30*6)
    expense= Expense.objects.filter(owner=requests.user,
        date__gte=six_month_ago,date__lte=today_date
    )
    finalrep={}
    def get_category(expense):
        return expense.category
    category_list=list(set(map(get_category,expense))) 
    def get_expense_category_amount(category):
        amount=0
        filter_by_category=expense.filter(category=category)
        for item in filter_by_category:
            amount+=item.amount
        return amount
    for x in expense:
        for y in category_list:
            finalrep[y] = get_expense_category_amount(y)  
    return  JsonResponse({'expense_category':finalrep})          

def statsView(request):
    return render(request,'expense/stats.html')    

#output pdf
def export_pdf(requests):
    response=HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=Expenses' + \
        str(datetime.datetime.now()) +'.pdf'
    response['Content-Transfer-Encoding'] = 'binary'
    expenses=Expense.objects.filter(owner=requests.user)
    sum=expenses.aggregate(Sum('amount'))
    html_string=render_to_string(
        'expense/pdf-output.html',{'expenses':expenses,'total':sum['amount__sum']}
    )  
    html=HTML(string=html_string)  
    result=html.write_pdf()

    with tempfile.NamedTemporaryFile(delete=True) as output:
        output.write(result)
        output.flush()
        output = open(output.name,'rb')
        response.write(output.read())
    return response    


#search function
def Search(requests):
    query=requests.POST['search']
    page_number=requests.GET.get('page')
    expense = Expense.objects.filter(category__icontains=query)
    paginator=Paginator(expense,4)
         
    page_obj=Paginator.get_page(paginator,page_number)
    if expense:
        context={'expens':expense,'page_obj':page_obj}
    else:
        context={'expens':expense,'page_obj':page_obj,'search':'fgty'}    

    return render(requests,'expense/index.html',context)
    
    
