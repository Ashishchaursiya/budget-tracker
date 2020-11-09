from django.urls import path
from . import views


urlpatterns = [
    path('',views.home,name='expense'),
    path('add-expense',views.Add_Expense,name='add-expense'),
    path('edit-expense/<int:id>',views.Edit_Expense,name='edit-expense'),
    path('delete-expense/<int:id>',views.Delete_Expense,name='delete-expense'),
    path('expense-summary',views.expense_category_summary,name='expense-summary'),
    path('stats',views.statsView,name='stats'),
    path('export-pdf',views.export_pdf,name='export-pdf'),
    path('expense-search',views.Search,name='expense-search'),

]