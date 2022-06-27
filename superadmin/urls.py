from django.urls import path
from superadmin import views
app_name="App_Admin"
urlpatterns = [
    path('',views.Dashboard,name="dashboard"),
    path('sales-list',views.SalesList,name="saleslist"),
    path('bill-list',views.AddExpense,name='addexpense'),
    path('categories',views.CategoryView,name='category'),
]