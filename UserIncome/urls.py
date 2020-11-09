from django.urls import path
from . import views


urlpatterns = [
    path('',views.home,name='income'),
    path('add-income',views.Add_Income,name='add-income'),
    path('edit-income/<int:id>',views.Edit_Income,name='edit-income'),
    path('delete-income/<int:id>',views.Delete_Income,name='delete-income'),
    path('search',views.Search,name='search'),
    path('income-summary',views.income_category_summary,name='income-summary'),
    path('income-stats',views.statsView,name='income-stats'),
    path('export-pdf',views.export_pdf,name='export-pdf'),

]